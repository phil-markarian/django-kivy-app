import requests
from kivy.clock import Clock
from kivy.uix.recycleview import RecycleView
from kivy.app import App

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout

#menu
class Menu(BoxLayout):
    pass
#screens
class HomeScreen(Screen):
    pass
class AddScreen(Screen):
    pass
#Screen Management
class ScreenManagement(ScreenManager):
    pass
#app class
class TodoApp(App):
    pass
#recycle view for home screen
class MyRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(MyRecycleView, self).__init__(**kwargs)
        self.load_data()
        Clock.schedule_interval(self.load_data, 1)
    def load_data(self, *args):
        store = requests.get('http://127.0.0.1:8000/').json()

        list_data = []
        for item in store:
            list_data.append({'text': item['name']})

        self.data = list_data

if __name__ == '__main__':
    TodoApp().run()