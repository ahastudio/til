# Roo: Ruby로 스프레드시트를 읽는 젬

<https://github.com/roo-rb/roo>

## 소개

Roo는 여러 스프레드시트 형식을 하나의 인터페이스로 읽는 Ruby 젬이다.
README가 밝히는 범위는 읽기 전용이다.
쓰기와 편집은 이 젬의 일이 아니다.

기본 젬이 직접 다루는 형식은 xlsx, xlsm, ods, csv다.
옛 Excel 형식(xls, Excel 2002/2003 XML)은 `roo-xls` 젬을 따로 설치해야 하고,
Google 스프레드시트는 `roo-google` 젬이 맡는다.
README는 후자에 한해 읽기와 쓰기 접근을 제공한다고 적는다.

저장소는 MIT 라이선스이고 README 기준 현재 젬 버전은 3.0.0이다.
README는 Ruby 3.x 지원을 개선할 다음 주요 릴리스를 계획하고 있다며,
의견은 이슈 630번에 남기라고 안내한다.
다음 주요 릴리스가 아직 나오지 않았다는 뜻이므로
새 프로젝트에 넣을 때는 사용하는 Ruby 버전에서 먼저 돌려 보아야 한다.

## 설치하기

```bash
gem install roo
```

Gemfile에서는 README가 예시로 든 버전 제약을 쓴다.

```ruby
gem "roo", "~> 3.0.0"
```

xls 파일이나 Google 스프레드시트가 필요하면 `roo-xls`, `roo-google`을 추가한다.
Roo 1.13.x에서 버전을 올리는 경우 이 두 기능이 본체에서 분리되었으므로,
README는 변경 이력(Changelog)을 먼저 보라고 한다.

## 파일 열기

`Roo::Spreadsheet.open`은 확장자를 보고 알맞은 파서 클래스를 고른다.
문자열 경로와 `File` 객체를 모두 받는다.

```ruby
require 'roo'

xlsx = Roo::Spreadsheet.open('./new_prices.xlsx')
xlsx.info
```

업로드된 임시 파일처럼 확장자가 없으면 `extension`을 직접 알려 준다.

```ruby
xlsx = Roo::Spreadsheet.open('./rails_temp_upload', extension: :xlsx)
```

형식을 이미 알면 파서 클래스인 `Roo::Excelx`,
`Roo::OpenOffice`, `Roo::CSV`를 바로 쓴다.

## 시트와 셀 다루기

행, 열, 셀 번호는 Excel 방식이라 0이 아니라 1에서 시작한다.
`Array` 인덱스와 다르므로 가장 먼저 어긋나는 지점이다.

```ruby
sheet.sheets                # 시트 이름 배열
sheet.default_sheet = 'Sheet 3'

sheet.row(1)                # 첫 행
sheet.column(1)             # 첫 열
sheet.first_row             # 첫 행 번호
sheet.last_row              # 마지막 행 번호

sheet.cell(1, 1)            # 왼쪽 위 셀
sheet.cell('A', 1)          # 열 문자와 행 번호도 가능
sheet.a1                    # 같은 셀
```

대부분의 메서드는 선택 인자로 시트를 받고,
생략하면 `default_sheet`를 쓴다.
시트를 바꿔 가며 읽는 코드에서는 이 암묵적 상태가 버그의 원인이 되기 쉽다.
`each_with_pagename`으로 순회하거나 시트를 인자로 명시하는 편이 안전하다.

## 행을 해시로 읽기

`each`에 열 이름을 해시로 주면 행마다 해시를 만들어 준다.
`parse`는 같은 결과를 배열에 담아 돌려준다.
열 이름은 문자열이나 정규식으로 지정한다.

```ruby
sheet.each(id: 'ID', name: 'FULL_NAME') do |hash|
  puts hash.inspect
end

sheet.parse(id: /UPC|SKU/, qty: /ATS*\sATP\s*QTY\z/)
```

`parse`의 옵션은 세 가지다.

- `headers: true`는 머리글 행을 결과에 포함한다.
- `header_search`는 정규식 목록으로 머리글 행을 찾아 이름을 정한다.
- `clean: true`는 제어 문자와 앞뒤 공백을 지운다.

머리글이 첫 행이 아닌 시트에서는 `header_search`가 필요하다.

## 큰 xlsx 스트리밍하기

`Roo::Excelx`는 행을 하나씩 스트리밍으로 읽는 `each_row_streaming`을 제공한다.
기본값에서는 빈 셀을 배열에서 뺀다.
위치를 유지해야 하면 `pad_cells: true`로 빈 셀을 `nil`로 채운다.

```ruby
xlsx = Roo::Excelx.new('./big.xlsx')

xlsx.each_row_streaming(offset: 1, pad_cells: true) do |row|
  # row는 Roo::Excelx::Cell 객체의 배열이다
  puts row.map { |cell| cell&.value }.inspect
end
```

`offset: 1`은 머리글 행을 건너뛴다.
`max_rows`는 offset 뒤로 읽을 행 수를 정하는데,
README에 따르면 자동으로 1이 더해져 `max_rows: 3`이면 네 행이 나온다.
이 대목은 문서에 적힌 동작이므로 직접 돌려서 확인한 뒤 의존하는 것이 좋다.

## 셀 값과 서식

`Roo::Excelx`로는 셀의 종류, 주석, 글꼴,
수식, 하이퍼링크, 레이블에 접근할 수 있다.
같은 셀을 세 가지 값으로 볼 수 있다는 점이 핵심이다.

```ruby
xlsx.cell(3, 'C')            # 600000383.0 (숫자로 읽은 값)
xlsx.excelx_value(3, 'C')    # '600000383' (파일에 저장된 값)
xlsx.formatted_value(3, 'C') # '0600000383' (서식을 적용한 값)
```

우편번호나 관리 번호처럼 앞자리 0에 의미가 있는 열은 `cell`로 읽으면
숫자가 되어 0이 사라진다.
이런 열은 `formatted_value`로 읽어야 한다.

병합된 셀은 첫 칸 외에는 `nil`로 나온다.
이를 피하려면 파일을 열 때 옵션을 준다.

```ruby
xlsx = Roo::Excelx.new('./merged.xlsx', expand_merged_ranges: true)
```

## CSV와 ODS

CSV는 표준 CSV 라이브러리로 읽으므로 그 옵션을 `csv_options`로 넘긴다.

```ruby
tsv = Roo::CSV.new('data.tsv', csv_options: { col_sep: "\t" })

# Excel이 저장한 CSV의 BOM을 떼고 읽는다
csv = Roo::Spreadsheet.open('data.csv',
                            csv_options: { encoding: 'bom|utf-8' })
```

암호가 걸린 OpenOffice 파일은 `password:` 옵션으로 연다.

```ruby
ods = Roo::OpenOffice.new('myspreadsheet.ods', password: 'password')
```

## 내보내기

`to_csv`, `to_matrix`, `to_xml`, `to_yaml`로 내보낼 수 있다.
README에 따르면 이 메서드들은 `default_sheet` 하나만 내보낸다.
통합 문서 전체를 내보내려면 시트를 돌며 `default_sheet`를 바꿔 호출해야 한다.

## 함정

- 1부터 시작하는 번호는 `0`을 넣어도 오류 없이 엉뚱한 결과를 낼 수 있다.
- `default_sheet`는 객체에 붙은 상태라 여러 곳이 공유하면 서로 간섭한다.
- 읽기 전용이므로 결과 파일을 만드는 용도로는 다른 젬이 따로 필요하다.
- 사용자가 올린 파일은 확장자와 내용이 다를 수 있으므로
  `extension` 지정과 예외 처리를 함께 둔다.
- 앞자리 0이 있는 숫자형 열은 `cell` 값만 믿으면 데이터가 바뀐다.

## 확인하기

작은 xlsx 파일 하나로 아래 코드를 돌리면 이 노트에서
다룬 동작 중 가장 어긋나기 쉬운 부분을 한 번에 확인할 수 있다.

```ruby
require 'roo'

x = Roo::Spreadsheet.open('sample.xlsx')
p x.sheets
p [x.first_row, x.last_row]
p x.cell(1, 1)
p x.formatted_value(2, 1)

x.each_row_streaming(max_rows: 3) { |r| p r.size }
```

## 체크리스트

- 읽어야 하는 형식이 xls나 Google 스프레드시트라면 해당 젬을 Gemfile에 넣었는가.
- 사용 중인 Ruby 버전에서 테스트가 통과하는가.
- 앞자리 0이 있는 열을 `formatted_value`로 읽는가.
- 병합 셀이 있는 파일에 `expand_merged_ranges`를 줬는가.
- 큰 파일을 `each_row_streaming`으로 읽는가.
- 시트를 암묵적 `default_sheet`가 아니라 명시적으로 지정하는가.

## 기억할 원칙

### 읽는 값과 보이는 값은 다르다

스프레드시트의 셀은 저장된 값, 해석한 값, 화면에 보이는 값이 서로 다를 수 있다.
Roo가 세 가지 접근자를 따로 두는 이유다.
어느 값이 업무상 진실인지 먼저 정하고 그에 맞는 접근자를 고르면
앞자리 0이 사라지는 종류의 오류를 막는다.
