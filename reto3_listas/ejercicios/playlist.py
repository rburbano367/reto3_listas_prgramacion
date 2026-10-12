class Nodo:
    def __init__(self, titulo):
        self.titulo = titulo
        self.siguiente = None


class PlaylistCircular:
    def __init__(self):
        self.head = None

    def insertar_cola(self, titulo):
        nuevo = Nodo(titulo)
        if self.head is None:
            self.head = nuevo
            nuevo.siguiente = nuevo
        else:
            actual = self.head
            while actual.siguiente != self.head:
                actual = actual.siguiente
            actual.siguiente = nuevo
            nuevo.siguiente = self.head
        print(f"🎵 Canción '{titulo}' agregada a la playlist")

    def reproducir(self, repeticiones=2):
        if self.head is None:
            print("!!!!!! Playlist vacia")
            return
        actual = self.head
        for r in range(repeticiones):
            print(f"Reproducción {r + 1}")
            while True:
                print(f"  >>>>>>> Reproduciendo: {actual.titulo}")
                actual = actual.siguiente
                if actual == self.head:
                    break


if __name__ == "__main__":
    playlist = PlaylistCircular()
    playlist.insertar_cola("Song A")
    playlist.insertar_cola("Song B")
    playlist.insertar_cola("Song C")
    playlist.reproducir(2)
