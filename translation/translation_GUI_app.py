import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtCore import QRunnable, QThreadPool, pyqtSlot, pyqtSignal, QObject
from translation_input_app import Translator

# 백그라운드 작업의 신호를 정의하는 클래스
class TranslateWorkerSignals(QObject):
    finished = pyqtSignal()  # 작업 완료 신호
    error = pyqtSignal(tuple)  # 오류 발생 시 신호
    result = pyqtSignal(str)  # 결과 반환 신호

# 번역 작업을 처리할 QRunnable 클래스
class TranslateWorker(QRunnable):
    def __init__(self, text):
        super().__init__()
        self.text = text  # 번역할 텍스트
        self.signals = TranslateWorkerSignals()  # 신호 객체 생성

    @pyqtSlot()
    def run(self):
        try:
            translator = Translator()  # 번역기 객체 생성
            translated_text = translator.translate_to_korean(self.text)  # 번역 실행
            self.signals.result.emit(translated_text)  # 번역 결과 신호 송출
        except Exception as e:
            self.signals.error.emit((e,))  # 오류 발생 시 신호 송출

# 메인 어플리케이션 클래스
class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()  # UI 초기화
        self.thread_pool = QThreadPool()  # 스레드 풀 생성

    def initUI(self):
        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()

        # 상단 레이아웃 설정
        top_layout = QHBoxLayout()
        lbl_input = QLabel('영어문장을 입력해주세요.')  # 입력 라벨
        lbl_output = QLabel('한글 번역 결과')  # 출력 라벨
        top_layout.addWidget(lbl_input)
        top_layout.addStretch(1)  # 중간에 빈 공간 추가
        top_layout.addWidget(lbl_output)

        # 중앙 레이아웃 설정
        center_layout = QHBoxLayout()
        self.text_input = QTextEdit()  # 입력 텍스트 영역
        self.text_output = QTextEdit()  # 출력 텍스트 영역
        self.text_output.setReadOnly(True)  # 출력 텍스트 영역을 읽기 전용으로 설정
        center_layout.addWidget(self.text_input)
        center_layout.addWidget(self.text_output)

        # 하단 레이아웃 설정
        bottom_layout = QHBoxLayout()
        self.translate_button = QPushButton('번역 요청 버튼')  # 번역 요청 버튼
        self.translate_button.clicked.connect(self.translate_text)  # 버튼 클릭 시 번역 함수 호출
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.translate_button)

        # 메인 레이아웃에 하위 레이아웃 추가
        main_layout.addLayout(top_layout)
        main_layout.addLayout(center_layout)
        main_layout.addLayout(bottom_layout)

        # 메인 윈도우 설정
        self.setLayout(main_layout)
        self.setWindowTitle('영어 -> 한글 번역기')  # 윈도우 제목 설정
        self.setGeometry(300, 300, 800, 400)  # 윈도우 위치 및 크기 설정
        self.show()  # 윈도우 표시

    def translate_text(self):
        input_text = self.text_input.toPlainText()  # 입력된 텍스트 가져오기
        worker = TranslateWorker(input_text)  # 번역 작업 객체 생성
        worker.signals.result.connect(self.display_translation)  # 번역 결과 신호 연결
        worker.signals.error.connect(self.handle_error)  # 오류 발생 신호 연결
        self.thread_pool.start(worker)  # 스레드 풀에서 작업 시작

    def display_translation(self, translated_text):
        self.text_output.setPlainText(translated_text + " (번역됨)")  # 번역된 텍스트 표시

    def handle_error(self, error):
        self.text_output.setPlainText(f"Error: {error}")  # 오류 메시지 표시

if __name__ == '__main__':
    app = QApplication(sys.argv)  # QApplication 객체 생성
    ex = TranslatorApp()  # TranslatorApp 객체 생성
    sys.exit(app.exec_())  # 이벤트 루프 실행
