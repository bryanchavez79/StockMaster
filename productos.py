import sqlite3
from dataclasses import dataclass

@dataclass
class Producto:
    codigo: str
    nombre: str
    categoria: str
    precio: float
    stock: int

    def __post_init__(self):
        self.codigo = self.codigo.strip()
        self.nombre = self.nombre.strip()
        self.categoria = self.categoria.strip()

        if not self.codigo:
            raise ValueError("El código no puede estar vacío.")
        if not self.nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if not self.categoria:
            raise ValueError("La categoría no puede estar vacía.")
        if self.precio < 0:
            raise ValueError("El precio debe ser mayor o igual a 0.")
        if self.stock < 0:
            raise ValueError("El stock debe ser mayor o igual a 0.")

    def __str__(self) -> str:
        return (
            f"{self.codigo} - {self.nombre} | {self.categoria} | "
            f"${self.precio:.2f} | stock: {self.stock}"
        )

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
        }

    @classmethod
    def from_row(cls, row: tuple | sqlite3.Row) -> "Producto":
        if row is None:
            raise ValueError("No se recibió una fila válida para crear el producto.")

        if isinstance(row, sqlite3.Row):
            return cls(
                codigo=row["codigo"],
                nombre=row["nombre"],
                categoria=row["categoria"],
                precio=row["precio"],
                stock=row["stock"],
            )

        return cls(
            codigo=row[0],
            nombre=row[1],
            categoria=row[2],
            precio=row[3],
            stock=row[4],
        )
