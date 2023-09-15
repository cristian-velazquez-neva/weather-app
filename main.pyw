from tkinter import ttk
from tkinter import messagebox

import geonamescache as gc
import datetime as dt
import tkinter as tk
import requests

class WeatherApp:
	def __init__(self, master):
		self.master = master
		self.city = tk.StringVar()
		self.city.set("Mexico")

		self.gc = gc.GeonamesCache()

		self.create_gui()
		self.get_weather()

	def create_gui(self):
		self.frame = tk.Frame(self.master)
		self.frame.pack()

		tk.Label(self.frame, text='Weather App', font = ('default', 10, 'bold')).grid(row=0, pady=5, sticky='we')

		self.escity = tk.Frame(self.frame)
		self.escity.grid(row=1, padx=10, pady=5, sticky='we')

		tk.Label(self.escity, text='Enter or Select a City:').grid(row=0, sticky='w')

		self.cities = ttk.Combobox(self.escity, values=[city['name'] for city in self.gc.get_cities().values()])
		self.cities.set(self.city.get())
		self.cities.bind('<Return>', self.change_city)
		self.cities.bind('<<ComboboxSelected>>', self.change_city)
		self.cities.grid(row=1, sticky='we')

		self.frame_grades = tk.Frame(self.frame)
		self.frame_grades.grid(row=2)

		self.celsius = tk.Label(self.frame_grades, font=('default', 12, 'bold'))
		self.celsius.grid(padx=10, pady=5, sticky='we')

		self.fahrenheit = tk.Label(self.frame_grades, font=('default', 12, 'bold'))
		self.fahrenheit.grid(row=0, column=1, padx=10, pady=5, sticky='we')

		self.description_icon = tk.Label(self.frame, font=('default', 36))
		self.description_icon.grid(row=3, pady=8, sticky='we')

		self.description = tk.Label(self.frame, font=('default', 10, 'bold'))
		self.description.grid(row=4, sticky='we')

		self.weather = tk.Label(self.frame, justify="left")
		self.weather.grid(row=5, padx=5, pady=5, sticky='w')

	def change_city(self, event):
		try:
			self.city.set(event.widget.get())
			self.get_weather()
		except KeyError:
			messagebox.showwarning('Warning', 'City not found')

	def get_weather(self):
		BASE_URL = "http://api.openweathermap.org/data/2.5/weather/?"
		API_KEY = open('api_key', 'r').read()
		url = BASE_URL + "appid=" + API_KEY + "&q=" + self.city.get()
		response = requests.get(url).json()

		temp_kelvin = response['main']['temp']
		temp_celsius, temp_fahrenheit = self.kelvin_to_celsius_fahrenheit(temp_kelvin)

		description = response['weather'][0]['description']
		wind_speed = response['wind']['speed']
		humidity = response['main']['humidity']

		self.celsius.config(text=f"{temp_celsius:.0f}°C")
		self.fahrenheit.config(text=f"{temp_fahrenheit:.0f}°F")

		if description == "clear sky":
			self.description_icon.config(text="🔆")
		elif description == "broken clouds" or description == "overcast clouds":
			self.description_icon.config(text="⛅")
		elif description == "moderate rain" or description == "light rain":
			self.description_icon.config(text="☔")
		elif description == "few clouds" or description == "scattered clouds":
			self.description_icon.config(text="🌁")
		else:
			self.description_icon.config(text="")
		self.description.config(text=description.capitalize())

		self.weather.config(text= f"Humidity: {humidity}%\nWind Speed: {wind_speed}m/s")

	def kelvin_to_celsius_fahrenheit(self, kelvin):
		celsius = kelvin - 273.15
		fahrenheit = celsius * (9/5) + 32
		return celsius, fahrenheit

if __name__ == '__main__':
	root = tk.Tk()
	root.title('Weather App')
	root.resizable(False, False)
	WeatherApp(root)
	root.mainloop()