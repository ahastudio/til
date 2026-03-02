# Moonshine - 실시간 음성 인식 툴킷

<https://github.com/moonshine-ai/moonshine>

Moonshine AI가 만든 오픈소스 음성 인식(ASR) 툴킷.
실시간 음성 애플리케이션을 위해 설계되었으며, 온디바이스로
동작하여 API 키나 클라우드 서비스 없이 빠르고 프라이빗한
처리가 가능하다.

## 핵심 특징

- **온디바이스 처리**: 모든 처리가 로컬에서 이루어진다.
  API 키, 계정, 클라우드 의존성이 없다.
- **스트리밍 최적화**: 사용자가 말하는 도중에도 저지연으로
  응답한다. 고정 30초 윈도우 대신 가변 길이 오디오를
  받아들인다.
- **상태 캐싱**: 인코더와 디코더 상태를 캐싱하여 증분
  처리한다. 중복 연산을 줄여 지연 시간을 단축한다.
- **크로스 플랫폼**: Python, iOS, Android, macOS, Linux,
  Windows, Raspberry Pi, IoT 디바이스를 지원한다.
- **다국어 지원**: 영어, 스페인어, 중국어(만다린), 일본어,
  한국어, 베트남어, 우크라이나어, 아랍어.

## 아키텍처

C++ 코어 라이브러리 위에 각 플랫폼별 바인딩(Python,
Swift, Java, C++)을 제공하는 구조다.
추론 엔진으로 OnnxRuntime을 사용한다.

### 처리 파이프라인

```text
마이크 입력 → 음성 활동 감지(VAD)
→ 음성-텍스트 변환(STT) → 화자 식별
→ 의도 인식(Intent Recognition)
```

단일 라이브러리에 전체 파이프라인이 통합되어 있다.

### 이벤트 기반 인터페이스

애플리케이션은 원시 오디오가 아닌 구조화된 이벤트를
받는다.

- **LineStarted**: 발화 시작 시 호출.
- **LineTextChanged**: 텍스트가 업데이트될 때 호출.
- **LineCompleted**: 화자가 멈추고 구간이 완료될 때 호출.

스트림당 한 번에 하나의 활성 라인만 존재한다.

## 성능 벤치마크

Whisper와 비교한 영어 음성 인식 성능이다.

| 모델                       | WER    | 파라미터 | MacBook Pro | Linux x86 | R. Pi 5  |
| -------------------------- | ------ | -------- | ----------- | --------- | -------- |
| Moonshine Medium Streaming | 6.65%  | 245M     | 107ms       | 269ms     | 802ms    |
| Whisper Large v3           | 7.44%  | 1.5B     | 11,286ms    | 16,919ms  | N/A      |
| Moonshine Small Streaming  | 7.84%  | 123M     | 73ms        | 165ms     | 527ms    |
| Whisper Small              | 8.59%  | 244M     | 1,940ms     | 3,425ms   | 10,397ms |
| Moonshine Tiny Streaming   | 12.00% | 34M      | 34ms        | 69ms      | 237ms    |
| Whisper Tiny               | 12.81% | 39M      | 277ms       | 1,141ms   | 5,863ms  |

Moonshine Medium는 Whisper Large v3보다 **WER이 낮으면서
파라미터는 6분의 1**, 추론 속도는 100배 이상 빠르다.
실시간 음성 인터페이스에서 결정적인 차이다.

## 모델 구성

언어별 전용 모델을 학습한다. 통합 다국어 모델 대비
정확도가 높고 크기가 작다.

- **Tiny**: 34M 파라미터, 약 26MB.
- **Small**: 123M 파라미터.
- **Medium**: 245M 파라미터.

## 의도 인식 (Intent Recognition)

Gemma 300M 기반 문장 임베딩 모델을 사용하여 시맨틱
매칭으로 사용자 의도를 인식한다. 정확한 문구 일치가
아니라 의미적 유사도로 매칭한다.

```text
📝 "Let there be light."
→ 'TURN ON THE LIGHTS' (76% confidence)
```

임계값(threshold) 파라미터로 매칭 민감도를 조절한다.
낮으면 더 많이 매칭되지만 정확도가 떨어진다.

## 사용법

```bash
pip install moonshine-voice
python -m moonshine_voice.mic_transcriber --language en
```

```python
class MyListener(TranscriptEventListener):
    def on_line_started(self, event):
        print(f"시작: {event.line.text}")

    def on_line_text_changed(self, event):
        print(f"변경: {event.line.text}")

    def on_line_completed(self, event):
        print(f"완료: {event.line.text}")

transcriber = Transcriber(
    model_path=model_path,
    model_arch=model_arch,
)
transcriber.add_listener(MyListener())
transcriber.start()
```

오디오를 청크 단위로 전달하면 이벤트 콜백이 호출된다.

## Whisper와 비교

| 항목         | Moonshine              | Whisper            |
| ------------ | ---------------------- | ------------------ |
| 입력 방식    | 가변 길이, 스트리밍    | 고정 30초 윈도우   |
| 처리 방식    | 증분 캐싱, 상태 유지   | 전체 윈도우 재처리 |
| 모델 전략    | 언어별 전용 모델       | 단일 다국어 모델   |
| 실행 환경    | 온디바이스             | 온디바이스/클라우드 |
| 실시간 지원  | 네이티브               | 추가 구현 필요     |
| 정확도(영어) | 6.65% WER (Medium)     | 7.44% WER (Large)  |
| 추론 속도    | 107ms (Medium, M. Pro) | 11,286ms (Large)   |

## 논문

- [Moonshine 연구 논문](https://arxiv.org/abs/2602.12241)
- [Flavors of Moonshine](https://arxiv.org/abs/2509.02523)
- [1세대 모델](https://arxiv.org/abs/2410.15608)

## 관련 링크

- [OpenASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)
- [Discord 커뮤니티](https://discord.gg/27qp9zSRXF)
