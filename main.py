import requests
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.recycleview import RecycleView  # Import RecycleView
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
import json


class Menu(BoxLayout):
    pass






class MyRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(MyRecycleView, self).__init__(**kwargs)

        # Load data initially
        self.load_data()

        # Schedule the load_data method to run every 1 second
        Clock.schedule_interval(self.load_data, 1)

    def load_data(self, *args):
        try:
            app = App.get_running_app()

            # Check if the user is logged in (token is not empty)
            if not app.token:
                print("DEBUG: User is not logged in. Skipping data loading.")
                return

            # Use the correct endpoint for fetching tasks
            endpoint = 'http://127.0.0.1:8000/all_tasks/'  # Adjust the endpoint as needed
            headers = {'Authorization': f'Token {app.token}'}
            response = requests.get(endpoint, headers=headers)

            # Check if the request was successful (status code 200)
            if response.ok:
                # Update the data property with the new tasks
                tasks = response.json()
                self.data = [{'text': item['name']} for item in tasks]

              # Print tasks
              #  print("DEBUG: Tasks:")
              #  for task in tasks:
              #      print(task)

                #print(f"DEBUG: Successfully retrieved {len(tasks)} tasks.")
            else:
                print(f"DEBUG: Error loading data - {response.status_code}: {response.text}")

        except Exception as e:
            print(f"DEBUG: Error loading data - {str(e)}")





class MyLabel(Label):
    pass


class HomeScreen(Screen):
    def on_pre_enter(self, *args):
        super(HomeScreen, self).on_pre_enter(*args)
        print("DEBUG: Pre-entering HomeScreen")

        # Remove existing MyRecycleView if it exists
        if hasattr(self, 'my_recycle_view'):
            self.remove_widget(self.my_recycle_view)

        # Create a new MyRecycleView instance
        self.my_recycle_view = MyRecycleView()
        self.add_widget(self.my_recycle_view)


class AddNewForm(Widget):
    text_input = ObjectProperty(None)
    input = StringProperty('')

    def submit_input(self):
        self.input = self.text_input.text
        app = App.get_running_app()
        headers = {'Content-Type': 'application/json', 'Authorization': f'Token {app.token}'}
        post = requests.post('http://127.0.0.1:8000/create/', json={'name': self.input}, headers=headers)
        print(post.request.method)  
        self.input = ''


class AddScreen(Screen):
    def __init__(self, **kwargs):
        super(AddScreen, self).__init__(**kwargs)
        self.box = BoxLayout()
        self.box.orientation = "vertical"
        self.box.add_widget(Label(text="Add To List...", color="blue", pos_hint={"top": 1}))
        self.addNewForm = AddNewForm()
        self.box.add_widget(self.addNewForm)
        self.add_widget(self.box)



class UserRegistrationScreen(Screen):
    username_input = ObjectProperty()
    password_input = ObjectProperty()
    email_input = ObjectProperty()

    def register_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        email = self.email_input.text

        if username and password and email:
            data = {
                'username': username,
                'password': password,
                'email': email
            }
            response = requests.post('http://127.0.0.1:8000/users/register/', json=data)

            if response.status_code == 201:
                print('User registered successfully!')

                # Access the app instance and its manager
                app = App.get_running_app()
                manager = app.root.ids.screen_manager

                # Check if manager is a valid ScreenManager instance
                if isinstance(manager, ScreenManager):
                    # Switch to the login screen
                    manager.current = 'screen_login'
                    print(f'Switched to login screen. Current screen: {manager.current}')
                else:
                    print('Invalid manager instance.')

            else:
                print('Registration failed.')
                # Handle the failure scenario, such as displaying an error message


class LoginScreen(Screen):
    def on_success(self, req, result):
        # Handle the successful response from the API or local logic
        print('Login successful')

        # Assuming your response JSON contains a 'token' field
        token = result.get('token', '')
        print(token)

        # Set the token in the app
        app = App.get_running_app()
        app.token = token

        # Switch to the user profile screen and pass the token
        screen_manager = app.root.ids.screen_manager
        screen_profile = screen_manager.get_screen('screen_profile')
        screen_profile.set_token(token)  # Call set_token to pass the token
        screen_manager.current = 'screen_profile'

    def on_failure(self, req, result):
        # Handle the failure response from the API or local logic
        print('Invalid username or password')
        # Display an error message or handle accordingly
    def login_user(self):
        username = self.username_input.text
        password = self.password_input.text

        if username and password:
            # Replace 'your_api_url' with the actual URL of your Django API endpoint
            api_url = 'http://127.0.0.1:8000/users/login/'

            # Data to be sent to the Django API
            data = {'username': username, 'password': password}

            # Send a POST request to the Django API
            response = requests.post(api_url, json=data)

            if response.status_code == 200:
                # Handle successful login
                self.on_success(None, response.json())
            elif response.status_code == 401:
                # Handle unsuccessful login
                self.on_failure(None, response.json())
            else:
                # Handle other response statuses
                print(response)
                print(f'Unexpected response status: {response.status_code}')
        else:
            print('Invalid username or password')
            # Display an error message or handle accordingly

class UserProfileScreen(Screen):
    username_label = ObjectProperty()
    email_label = ObjectProperty()
    token = ''  # Initialize the token as an empty string

    def set_token(self, token):
        self.token = token
        print(f'Token set in UserProfileScreen: {self.token}')  # Add this line to check if the token is set

    def on_pre_enter(self, *args):
        try:
            # Fetch user profile information
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get('http://127.0.0.1:8000/users/profile/', headers=headers)

            # Check if the request was successful (status code 200)
            if response.ok:
                user_profile_data = response.json()
                username = user_profile_data.get('username', '')
                email = user_profile_data.get('email', '')

                # Display user profile information
                user_profile_label_text = f"User Profile\nUsername: {username}\nEmail: {email}"
                self.username_label.text = f'Username: {username}'
                self.email_label.text = f'Email: {email}'
            else:
                # Handle unsuccessful API response
                print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            # Handle exceptions (network error, JSON parsing error, etc.)
            print(f"An error occurred: {e}")



class ScreenManagement(ScreenManager):
    pass


class TodoApp(App):
    token = ''  # Initialize the token as an empty string

    def on_success_login(self, req, result):
        # Handle successful login
        print('Login successful')
        self.token = result.get('token', '')  # Get the token from the response
        print(f'Token set: {self.token}')  # Add this line to check if the token is set
        # Add code to switch to the home screen or desired screen
        # Example: self.root.ids.screen_manager.current = 'screen_home'

        # Switch to the user profile screen and pass the token
        screen_manager = self.root.ids.screen_manager
        screen_profile = screen_manager.get_screen('screen_profile')
        screen_profile.set_token(self.token)

    def on_failure_login(self, req, result):
        # Handle unsuccessful login
        print('Invalid username or password')
        # Display an error message or handle accordingly

    def login_user(self, username, password):
        if username and password:
            # Replace 'your_api_url' with the actual URL of your Django API endpoint
            api_url = 'http://127.0.0.1:8000/users/login/'

            # Data to be sent to the Django API
            data = {'username': username, 'password': password}

            # Send a POST request to the Django API
            req = UrlRequest(api_url, on_success=self.on_success_login, on_failure=self.on_failure_login, req_body=json.dumps(data))
        else:
            print('Invalid username or password')
            # Display an error message or handle accordingly

    def on_pre_enter_screen_profile(self, *args):
        try:
            # Fetch user profile information
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get('http://127.0.0.1:8000/users/profile/', headers=headers)

            # Check if the request was successful (status code 200)
            if response.ok:
                user_profile_data = response.json()
                username = user_profile_data.get('username', '')
                email = user_profile_data.get('email', '')

                # Access the UserProfileScreen instance and set the labels
                screen_profile = self.root.ids.screen_manager.get_screen('screen_profile')
                screen_profile.ids.username_label.text = f'Username: {username}'
                screen_profile.ids.email_label.text = f'Email: {email}'

            else:
                # Handle unsuccessful API response
                print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            # Handle exceptions (network error, JSON parsing error, etc.)
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    TodoApp().run()
