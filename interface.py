from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.core.window import Window
import random
import time

Window.clearcolor = (1, 0.71, 0.85, 1)  # Fondo rosa Kirby

class KirbyPuzzle(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        # Estado del juego
        self.tiles = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.moves = 0
        self.start_time = None
        self.is_running = False
        
        # Colores inspirados en Kirby (RGB normalizado 0-1)
        self.colors = [
            (1, 0.41, 0.71, 1),      # #FF69B4
            (1, 0.71, 0.85, 1),      # #FFB6D9
            (1, 0.08, 0.58, 1),      # #FF1493
            (0.85, 0.44, 0.84, 1),   # #DA70D6
            (1, 0.44, 1, 1),         # #FF6FFF
            (1, 0.52, 0.76, 1),      # #FF85C1
            (1, 0.70, 0.85, 1),      # #FFB3D9
            (0.88, 0.40, 1, 1)       # #E066FF
        ]
        
        self.create_widgets()
        
    def create_widgets(self):
        # Título
        title = Label(
            text='⭐ Kirby 8-Puzzle ⭐',
            font_size='36sp',
            bold=True,
            size_hint_y=0.15,
            color=(1, 0.08, 0.58, 1)
        )
        self.add_widget(title)
        
        subtitle = Label(
            text='¡Ordena los números del 1 al 8!',
            font_size='16sp',
            size_hint_y=0.08,
            color=(0.55, 0, 0.55, 1)
        )
        self.add_widget(subtitle)
        
        # Panel de estadísticas
        stats_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.15,
            spacing=20
        )
        
        # Movimientos
        moves_box = BoxLayout(orientation='vertical')
        moves_box.add_widget(Label(
            text='Movimientos',
            font_size='14sp',
            color=(0.4, 0.4, 0.4, 1)
        ))
        self.moves_label = Label(
            text='0',
            font_size='32sp',
            bold=True,
            color=(1, 0.08, 0.58, 1)
        )
        moves_box.add_widget(self.moves_label)
        stats_layout.add_widget(moves_box)
        
        # Tiempo
        time_box = BoxLayout(orientation='vertical')
        time_box.add_widget(Label(
            text='Tiempo',
            font_size='14sp',
            color=(0.4, 0.4, 0.4, 1)
        ))
        self.time_label = Label(
            text='0:00',
            font_size='32sp',
            bold=True,
            color=(0.61, 0.19, 1, 1)
        )
        time_box.add_widget(self.time_label)
        stats_layout.add_widget(time_box)
        
        self.add_widget(stats_layout)
        
        # Tablero del puzzle
        self.board = GridLayout(
            cols=3,
            rows=3,
            spacing=8,
            padding=15,
            size_hint_y=0.5
        )
        
        self.buttons = []
        for i in range(9):
            btn = Button(
                font_size='48sp',
                bold=True,
                background_normal='',
                background_down=''
            )
            btn.bind(on_press=lambda x, idx=i: self.move_tile(idx))
            self.board.add_widget(btn)
            self.buttons.append(btn)
        
        self.add_widget(self.board)
        
        # Botones de control
        control_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.12,
            spacing=10
        )
        
        shuffle_btn = Button(
            text='🔀 Mezclar',
            font_size='18sp',
            bold=True,
            background_normal='',
            background_color=(1, 0.41, 0.71, 1)
        )
        shuffle_btn.bind(on_press=self.shuffle)
        control_layout.add_widget(shuffle_btn)
        
        reset_btn = Button(
            text='🔄 Reiniciar',
            font_size='18sp',
            bold=True,
            background_normal='',
            background_color=(0.85, 0.44, 0.84, 1)
        )
        reset_btn.bind(on_press=self.reset)
        control_layout.add_widget(reset_btn)
        
        self.add_widget(control_layout)
        
        # Instrucciones
        instructions = Label(
            text='💡 Haz clic en las fichas adyacentes al espacio vacío',
            font_size='12sp',
            size_hint_y=0.08,
            color=(0.4, 0.4, 0.4, 1)
        )
        self.add_widget(instructions)
        
        self.update_display()
    
    def update_display(self):
        """Actualiza la visualización del tablero"""
        for i, tile in enumerate(self.tiles):
            btn = self.buttons[i]
            if tile == 0:
                btn.text = ''
                btn.background_color = (0.88, 0.40, 1, 0.3)
                btn.disabled = True
            else:
                btn.text = str(tile)
                btn.background_color = self.colors[tile - 1]
                btn.color = (1, 1, 1, 1)
                btn.disabled = False
    
    def can_move(self, index):
        """Verifica si una ficha se puede mover"""
        empty_index = self.tiles.index(0)
        row = index // 3
        col = index % 3
        empty_row = empty_index // 3
        empty_col = empty_index % 3
        
        return (
            (row == empty_row and abs(col - empty_col) == 1) or
            (col == empty_col and abs(row - empty_row) == 1)
        )
    
    def move_tile(self, index):
        """Mueve una ficha si es posible"""
        if self.tiles[index] == 0 or not self.can_move(index):
            return
        
        # Iniciar temporizador en el primer movimiento
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time()
            Clock.schedule_interval(self.update_timer, 1)
        
        # Realizar el movimiento
        empty_index = self.tiles.index(0)
        self.tiles[index], self.tiles[empty_index] = self.tiles[empty_index], self.tiles[index]
        
        self.moves += 1
        self.moves_label.text = str(self.moves)
        
        self.update_display()
        self.check_win()
    
    def check_win(self):
        """Verifica si el jugador ha ganado"""
        if self.tiles == [1, 2, 3, 4, 5, 6, 7, 8, 0] and self.moves > 0:
            self.is_running = False
            Clock.unschedule(self.update_timer)
            
            content = BoxLayout(orientation='vertical', padding=20, spacing=20)
            content.add_widget(Label(
                text='🏆 ¡Felicidades! 🏆',
                font_size='28sp',
                bold=True,
                color=(1, 0.84, 0, 1)
            ))
            content.add_widget(Label(
                text=f'¡Has ganado!\n\nMovimientos: {self.moves}\nTiempo: {self.time_label.text}',
                font_size='18sp',
                halign='center'
            ))
            
            close_btn = Button(
                text='¡Genial! ⭐',
                size_hint_y=0.3,
                background_normal='',
                background_color=(1, 0.41, 0.71, 1),
                font_size='18sp',
                bold=True
            )
            content.add_widget(close_btn)
            
            popup = Popup(
                title='',
                content=content,
                size_hint=(0.8, 0.5),
                background_color=(1, 0.95, 0.8, 1)
            )
            close_btn.bind(on_press=popup.dismiss)
            popup.open()
    
    def shuffle(self, instance=None):
        """Mezcla el puzzle de forma aleatoria"""
        for _ in range(200):
            empty_index = self.tiles.index(0)
            neighbors = []
            
            if empty_index % 3 > 0:
                neighbors.append(empty_index - 1)
            if empty_index % 3 < 2:
                neighbors.append(empty_index + 1)
            if empty_index > 2:
                neighbors.append(empty_index - 3)
            if empty_index < 6:
                neighbors.append(empty_index + 3)
            
            random_neighbor = random.choice(neighbors)
            self.tiles[empty_index], self.tiles[random_neighbor] = \
                self.tiles[random_neighbor], self.tiles[empty_index]
        
        self.moves = 0
        self.moves_label.text = '0'
        self.is_running = False
        Clock.unschedule(self.update_timer)
        self.time_label.text = '0:00'
        
        self.update_display()
    
    def reset(self, instance=None):
        """Reinicia el juego al estado inicial"""
        self.tiles = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.moves = 0
        self.moves_label.text = '0'
        self.is_running = False
        Clock.unschedule(self.update_timer)
        self.time_label.text = '0:00'
        
        self.update_display()
    
    def update_timer(self, dt):
        """Actualiza el temporizador"""
        if self.is_running:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.time_label.text = f'{minutes}:{seconds:02d}'

class KirbyPuzzleApp(App):
    def build(self):
        self.title = 'Kirby 8-Puzzle'
        return KirbyPuzzle()

if __name__ == '__main__':
    KirbyPuzzleApp().run()