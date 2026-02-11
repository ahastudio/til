# Solid Queue

Rails 8부터 기본 Active Job 백엔드로 포함된
데이터베이스 기반 잡 큐 시스템이다.
Redis 같은 외부 의존성 없이 기존 데이터베이스만으로
백그라운드 작업을 처리할 수 있다.

## 특징

- Redis 없이 데이터베이스(PostgreSQL, MySQL, SQLite)만 사용
- `FOR UPDATE SKIP LOCKED`를 활용한 효율적인 폴링
- 동시성 제어(Concurrency Controls)
- 반복 작업(Recurring Jobs) 스케줄링
- 큐 일시 정지, 숫자 기반 우선순위
- 트랜잭션 무결성 보장
  (앱 데이터와 잡이 같은 DB에 있어 원자적 커밋 가능)
- 수평 확장 지원(여러 머신에서 워커 실행 가능)

## 설치

```bash
bundle add solid_queue
bin/rails solid_queue:install
```

설치하면 설정 파일과 마이그레이션이 생성된다.

## 설정

### Active Job 어댑터

```ruby
# config/environments/production.rb
config.active_job.queue_adapter = :solid_queue
```

### 데이터베이스 (config/database.yml)

```yaml
production:
  primary:
    <<: *default
    database: storage/production.sqlite3
  queue:
    <<: *default
    database: storage/production_queue.sqlite3
    migrations_paths: db/queue_migrate
```

### 워커와 디스패처 (config/queue.yml)

```yaml
production:
  dispatchers:
    - polling_interval: 1
      batch_size: 500
      concurrency_maintenance_interval: 300

  workers:
    - queues: "*"
      threads: 3
      processes: 1
      polling_interval: 0.1
    - queues: [critical, default]
      threads: 5
      processes: 2
```

워커의 `queues` 목록에서 순서가 중요하다.
앞쪽 큐의 잡이 모두 처리된 후에 다음 큐로 넘어간다.

## 잡 만들기

```ruby
class ReportJob < ApplicationJob
  queue_as :default

  def perform(user)
    report = Report.generate_for(user)
    ReportMailer.deliver(user, report).deliver_later
  end
end
```

```ruby
# 즉시 실행
ReportJob.perform_later(user)

# 지연 실행
ReportJob.set(wait: 1.hour).perform_later(user)

# 우선순위 지정 (숫자가 작을수록 높은 우선순위)
ReportJob.set(priority: 5).perform_later(user)
```

## 동시성 제어

`limits_concurrency`로 같은 키를 가진 잡의
동시 실행 수를 제한할 수 있다.

```ruby
class AccountSyncJob < ApplicationJob
  limits_concurrency to: 2,
                     key: ->(account) { account },
                     duration: 5.minutes

  def perform(account)
    account.sync_external_data
  end
end
```

- `to:` 최대 동시 실행 수
- `key:` 동시성을 구분하는 키
  (같은 키를 가진 잡끼리 제한)
- `duration:` 동시성 보장 시간
  (잡 실행이 이보다 길면 보장되지 않음)

### 잡 타입 간 동시성 제어

`group`을 사용하면 서로 다른 잡 클래스 간에도
동시성을 제어할 수 있다.

```ruby
class UserEmailJob < ApplicationJob
  limits_concurrency to: 1,
                     key: ->(user) { user.id },
                     duration: 15.minutes,
                     group: "UserOnboarding"

  def perform(user)
    # ...
  end
end

class UserSetupJob < ApplicationJob
  limits_concurrency to: 1,
                     key: ->(user) { user.id },
                     duration: 15.minutes,
                     group: "UserOnboarding"

  def perform(user)
    # ...
  end
end
```

같은 `group`과 `key`를 공유하는 잡은
하나만 실행된다.

## 반복 작업 (Recurring Jobs)

`config/recurring.yml`에 cron 형식으로 정의한다.

```yaml
production:
  daily_cleanup:
    class: CleanupJob
    schedule: "0 3 * * *"  # 매일 새벽 3시

  sync_inventory:
    class: InventorySyncJob
    schedule: "*/15 * * * *"  # 15분마다
    args: [100]

  monthly_report:
    class: MonthlyReportJob
    schedule: "0 9 1 * *"  # 매월 1일 오전 9시
```

스테이징이나 개발 환경에서 반복 작업을 비활성화하려면:

```bash
SOLID_QUEUE_SKIP_RECURRING=true bin/jobs
```

## 에러 처리

Active Job의 `retry_on`과 `discard_on`을 그대로 사용한다.

```ruby
class ExternalApiJob < ApplicationJob
  retry_on Net::OpenTimeout,
           wait: :polynomially_longer,
           attempts: 5

  discard_on ActiveJob::DeserializationError

  def perform(record)
    ExternalApi.sync(record)
  end
end
```

재시도 후에도 실패한 잡은 데이터베이스에 남으며,
Mission Control Jobs 대시보드로 확인하고
수동으로 재시도하거나 삭제할 수 있다.

```ruby
# Gemfile
gem "mission_control-jobs"
```

## 라이프사이클 훅

```ruby
SolidQueue.on_start { |supervisor| start_metrics }
SolidQueue.on_stop { |supervisor| stop_metrics }

SolidQueue.on_worker_start do |worker|
  Rails.logger.info "Worker started: #{worker.queues}"
end
```

사용 가능한 훅: `on_start`, `on_stop`,
`on_worker_start`, `on_worker_stop`,
`on_dispatcher_start`, `on_dispatcher_stop`,
`on_scheduler_start`, `on_scheduler_stop`

## 실행

```bash
# 기본 실행 (fork 모드)
bin/jobs

# async 모드 (스레드 기반, 단일 프로세스)
bin/jobs --mode async

# Puma 플러그인으로 함께 실행
# config/puma.rb
plugin :solid_queue
```

## 완전한 예제

주문 처리 시스템을 예로 들어보자.

### 잡 정의

```ruby
# app/jobs/process_order_job.rb
class ProcessOrderJob < ApplicationJob
  queue_as :critical

  limits_concurrency to: 1,
                     key: ->(order) { order.user_id },
                     duration: 10.minutes

  retry_on Stripe::RateLimitError,
           wait: :polynomially_longer,
           attempts: 3

  discard_on ActiveRecord::RecordNotFound

  def perform(order)
    ApplicationRecord.transaction do
      order.process_payment!
      order.update!(status: :paid)
      OrderConfirmationJob.perform_later(order)
      InventoryUpdateJob.perform_later(order)
    end
  end
end
```

```ruby
# app/jobs/order_confirmation_job.rb
class OrderConfirmationJob < ApplicationJob
  queue_as :default

  def perform(order)
    OrderMailer.confirmation(order).deliver_now
  end
end
```

```ruby
# app/jobs/inventory_update_job.rb
class InventoryUpdateJob < ApplicationJob
  queue_as :default

  limits_concurrency to: 5,
                     key: -> { "inventory" },
                     duration: 3.minutes

  def perform(order)
    order.line_items.each do |item|
      item.product.decrement!(:stock_count, item.quantity)
    end
  end
end
```

### 설정

```yaml
# config/queue.yml
production:
  dispatchers:
    - polling_interval: 1
      batch_size: 500

  workers:
    - queues: [critical]
      threads: 5
      processes: 2
    - queues: [default]
      threads: 3
      processes: 1
```

```yaml
# config/recurring.yml
production:
  stale_order_cleanup:
    class: StaleOrderCleanupJob
    schedule: "0 * * * *"  # 매시간

  daily_sales_report:
    class: DailySalesReportJob
    schedule: "0 6 * * *"  # 매일 오전 6시
```

### 컨트롤러에서 호출

```ruby
class OrdersController < ApplicationController
  def create
    @order = current_user.orders.create!(order_params)
    ProcessOrderJob.perform_later(@order)
    redirect_to @order, notice: "주문이 접수되었습니다."
  end
end
```

트랜잭션 무결성을 활용하면 주문 생성과
잡 등록을 원자적으로 처리할 수 있다.

```ruby
def create
  ApplicationRecord.transaction do
    @order = current_user.orders.create!(order_params)
    ProcessOrderJob.perform_later(@order)
  end
  redirect_to @order, notice: "주문이 접수되었습니다."
end
```

잡과 앱 데이터가 같은 데이터베이스에 있으므로,
트랜잭션이 롤백되면 잡 등록도 함께 롤백된다.
이것이 Redis 기반 큐에서는 불가능한
Solid Queue만의 장점이다.

---

- <https://github.com/rails/solid_queue>
- <https://guides.rubyonrails.org/active_job_basics.html>
- <https://github.com/rails/mission_control-jobs>
