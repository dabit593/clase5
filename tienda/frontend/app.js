const mensaje = document.getElementById("mensaje");
const tabla = document.getElementById("tabla-productos");
const sesion = document.getElementById("sesion");
const formCuenta = document.getElementById("form-cuenta");
const formLogin = document.getElementById("form-login");
const formProducto = document.getElementById("form-producto");

function pintarSesion() {
  const usuario = localStorage.getItem("usuario");
  const token = localStorage.getItem("token");

  if (usuario && token) {
    sesion.textContent = "Sesión iniciada: " + usuario;
    document.getElementById("btn-salir").style.display = "inline";
  } else {
    sesion.textContent = "No has iniciado sesión";
    document.getElementById("btn-salir").style.display = "none";
  }
}

function cargarProductos() {
  const token = localStorage.getItem("token");
  tabla.innerHTML = "";

  if (!token) {
    mensaje.textContent = "Inicia sesión para ver los productos";
    return;
  }

  fetch("/productos/", {
    headers: {
      Authorization: "Bearer " + token,
    },
  })
    .then((response) => response.json())
    .then((productos) => {
      productos.forEach((producto) => {
        const fila = document.createElement("tr");

        const nombre = document.createElement("td");
        nombre.textContent = producto.nombre;
        fila.appendChild(nombre);

        const descripcion = document.createElement("td");
        descripcion.textContent = producto.descripcion;
        fila.appendChild(descripcion);

        const precio = document.createElement("td");
        precio.textContent = producto.precio;
        fila.appendChild(precio);

        const stock = document.createElement("td");
        stock.textContent = producto.stock;
        fila.appendChild(stock);

        const acciones = document.createElement("td");

        const botonEditar = document.createElement("button");
        botonEditar.textContent = "Editar";
        botonEditar.addEventListener("click", () => {
          document.getElementById("id-producto").value = producto.id;
          document.getElementById("nombre").value = producto.nombre;
          document.getElementById("descripcion").value = producto.descripcion || "";
          document.getElementById("precio").value = producto.precio;
          document.getElementById("stock").value = producto.stock;
        });
        acciones.appendChild(botonEditar);

        const botonEliminar = document.createElement("button");
        botonEliminar.textContent = "Eliminar";
        botonEliminar.addEventListener("click", () => {
          fetch("/productos/" + producto.id, {
            method: "DELETE",
            headers: {
              Authorization: "Bearer " + token,
            },
          }).then((response) => {
            if (response.ok) {
              mensaje.textContent = "Producto eliminado";
              cargarProductos();
            } else {
              mensaje.textContent = "No se pudo eliminar el producto";
            }
          });
        });
        acciones.appendChild(botonEliminar);

        fila.appendChild(acciones);
        tabla.appendChild(fila);
      });
    });
}

formCuenta.addEventListener("submit", (evento) => {
  evento.preventDefault();

  const usuario = {
    username: document.getElementById("reg-usuario").value,
    email: document.getElementById("reg-email").value,
    password: document.getElementById("reg-password").value,
  };

  fetch("/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(usuario),
  })
    .then((response) => response.json())
    .then((datos) => {
      if (datos.id) {
        mensaje.textContent = "Cuenta creada. Ahora inicia sesión.";
        formCuenta.reset();
      } else {
        mensaje.textContent = datos.detail;
      }
    });
});

formLogin.addEventListener("submit", (evento) => {
  evento.preventDefault();

  const usuario = document.getElementById("login-usuario").value;
  const datosLogin = new URLSearchParams();
  datosLogin.append("username", usuario);
  datosLogin.append("password", document.getElementById("login-password").value);

  fetch("/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: datosLogin,
  })
    .then((response) => response.json())
    .then((datos) => {
      if (datos.access_token) {
        localStorage.setItem("token", datos.access_token);
        localStorage.setItem("usuario", usuario);
        mensaje.textContent = "Sesión iniciada";
        pintarSesion();
        cargarProductos();
      } else {
        mensaje.textContent = datos.detail;
      }
    });
});

document.getElementById("btn-salir").addEventListener("click", () => {
  localStorage.removeItem("token");
  localStorage.removeItem("usuario");
  mensaje.textContent = "Sesión cerrada";
  pintarSesion();
  tabla.innerHTML = "";
});

formProducto.addEventListener("submit", (evento) => {
  evento.preventDefault();

  const token = localStorage.getItem("token");

  if (!token) {
    mensaje.textContent = "Tienes que iniciar sesión";
    return;
  }

  const precio = document.getElementById("precio").value;
  const stock = document.getElementById("stock").value;

  if (precio === "" || stock === "" || isNaN(precio) || isNaN(stock)) {
    mensaje.textContent = "El precio y el stock deben ser números válidos";
    return;
  }

  const id = document.getElementById("id-producto").value;
  const producto = {
    nombre: document.getElementById("nombre").value,
    descripcion: document.getElementById("descripcion").value,
    precio: Number(precio),
    stock: Number(stock),
  };

  let url = "/productos/";
  let method = "POST";

  if (id) {
    url = "/productos/" + id;
    method = "PUT";
  }

  fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
    },
    body: JSON.stringify(producto),
  })
    .then((response) => response.json())
    .then((datos) => {
      if (datos.id) {
        mensaje.textContent = id ? "Producto actualizado" : "Producto creado";
        formProducto.reset();
        document.getElementById("id-producto").value = "";
        cargarProductos();
      } else {
        mensaje.textContent = "No se pudo guardar el producto";
      }
    });
});

document.getElementById("btn-cancelar").addEventListener("click", () => {
  formProducto.reset();
  document.getElementById("id-producto").value = "";
});

pintarSesion();
cargarProductos();
