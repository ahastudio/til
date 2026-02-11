# Solid Queue

Rails 8부터 기본 Active Job 백엔드로 포함된
데이터베이스 기반 잡 큐 시스템이다.
Redis 없이 기존 데이터베이스만으로 백그라운드 작업을 처리한다.

## 특징

- DB만 사용 (PostgreSQL, MySQL, SQLite)
- 동시성 제어 (`limits_concurrency`)
- 반복 작업 스케줄링 (`recurring.yml`)
- 트랜잭션 무결성
  (잡과 앱 데이터가 같은 DB라 원자적 커밋 가능)

## 예제: 주문 처리

### 잡

```ruby
# app/jobs/process_order_job.rb
class ProcessOrderJob < ApplicationJob
  queue_as :critical

  # 같은 유저의 주문은 한 번에 하나만 처리
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

### 컨트롤러

```ruby
class OrdersController < ApplicationController
  def create
    # 같은 트랜잭션 안에서 주문 생성 + 잡 등록.
    # 롤백되면 잡 등록도 함께 롤백된다.
    # Redis 기반 큐에서는 불가능한 부분.
    ApplicationRecord.transaction do
      @order = current_user.orders.create!(order_params)
      ProcessOrderJob.perform_later(@order)
    end
    redirect_to @order, notice: "주문이 접수되었습니다."
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
    schedule: "0 * * * *"

  daily_sales_report:
    class: DailySalesReportJob
    schedule: "0 6 * * *"
```

### 실행

```bash
bin/jobs
```

---

- <https://github.com/rails/solid_queue>
- <https://guides.rubyonrails.org/active_job_basics.html>
