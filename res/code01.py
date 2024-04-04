import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QListWidgetItem, QMenu, QInputDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit
from myAddDB import *

class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        # UI 파일 로드
        loadUi('res/mywin01.ui', self)

        self.setWindowTitle("DB로 만드는 주소록 VER 0.2")

        #DB 객체를 생성한다.
        self.db = mysqlDB()
        print (f'self.db객체는 {self.db}') #터미널에 확인

        # 나중에 할것
        #처음 실행시 self.db에서 주소록 데이터를 가져와서 보여주기

        # 버튼에 클릭 이벤트 연결

        self.addbtn.clicked.connect(self.addFunction)
        self.savebtn.clicked.connect(self.saveContacts)
        self.btnpicture.clicked.connect(self.getImage)

        # 이름과 전화번호, 이미지 파일 저장할 변수 초기화
        self.name = ""
        self.phone = ""
        self.image_path = ""

        # 기본 아이콘 설정
        self.default_icon = QIcon('res/default_image.png')
        self.imageLabel.setPixmap(self.default_icon.pixmap(128, 128))

        # 리스트 위젯에 우클릭 메뉴 추가
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.showContextMenu)

    def getImage(self):
        print("사진등록 버튼이 클릭되었습니다.")
        # 파일 다이얼로그 열기
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', './res', 'Images (*.png *.jpg *.jpeg *.bmp *.gif)')
        # 파일 선택되었는지 확인
        if filename:
            # 이미지 파일 경로 설정
            self.image_path = filename
            pixmap = QPixmap(self.image_path)
            # 이미지를 라벨에 표시
            self.imageLabel.setPixmap(pixmap)
            # 이미지 크기에 맞추기
            self.imageLabel.setScaledContents(True)
        else:
            # 선택한 이미지가 없는 경우, 기본 아이콘 설정
            self.imageLabel.setPixmap(self.default_icon.pixmap(128, 128))

    def addFunction(self):
        print("추가 버튼이 클릭되었습니다.")
        # 이름과 전화번호 저장
        self.name = self.nameEdit.text()
        self.phone = self.phoneEdit.text()

        # 이미지 파일이 선택되었는지 확인
        if self.image_path:
            # 이름과 전화번호가 비어있지 않으면 리스트 위젯에 추가
            if self.name and self.phone:
                item = QListWidgetItem()
                item.setText(f'Name: {self.name}, Phone: {self.phone}, Image: {self.image_path}')
                self.listWidget.addItem(item)

                #다 하고 나서 db에 쓰는 작업만 추가
                #result = self.db.inset(name, phone, filename) VALUES (%s, %s)
                #print (result)
            else:
                QMessageBox.warning(self, "경고", "이름과 전화번호를 모두 입력하세요.")
        else:
            QMessageBox.warning(self, "경고", "이미지를 선택하세요.")

    def saveContacts(self):
        print("저장 버튼이 클릭되었습니다.")
        # 파일 다이얼로그 열기
        #filename, _ = QFileDialog.getSaveFileName(self, 'Save File', './res', 'Text Files (*.txt)')
        filename = 'addbook.txt'
        # 파일 선택되었는지 확인
        if filename:
            # 주소록 데이터 준비
            contacts_data = []
            for index in range(self.listWidget.count()):
                item = self.listWidget.item(index)
                contacts_data.append(item.text())

            # 주소록 데이터를 파일에 저장
            with open(filename, 'w') as file:
                for contact in contacts_data:
                    file.write(contact + '\n')

    def showContextMenu(self, pos):
        menu = QMenu()
        delete_action = menu.addAction("삭제")
        modify_action = menu.addAction("수정")
        action = menu.exec_(self.listWidget.mapToGlobal(pos))
        if action == delete_action:
            self.deleteItem()
        elif action == modify_action:
            self.modifyItem()

    def deleteItem(self):
        row = self.listWidget.currentRow()
        if row >= 0:
            self.listWidget.takeItem(row)

    def modifyItem(self):
        row = self.listWidget.currentRow()
        if row >= 0:
            item = self.listWidget.item(row)
            new_text, ok = QInputDialog.getText(self, "항목 수정", "새로운 항목 내용:", QLineEdit.Normal, item.text())
            if ok and new_text:
                item.setText(new_text)
            else:
                QMessageBox.warning(self, "경고", "수정할 내용을 입력하세요.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MyMainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

