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

if __name__ == '__main__':
    TodoApp().run()