# Corrección de error GLX en Anaconda Navigator (Ubuntu + Intel UHD 620)

Guía práctica para resolver errores de inicialización GLX/Qt en **Anaconda Navigator** cuando se usa **GNOME (Wayland o Xorg)** con GPU **Intel UHD 620**.

---

## 🧭 Resumen
Si al ejecutar `anaconda-navigator` ves mensajes como:

```
qt.glx: qglx_findConfig: Failed to finding matching FBConfig...
Could not initialize GLX
```

o bien:

```
qt.qpa.plugin: Could not find the Qt platform plugin "wayland" in ""
```

sigue los pasos de esta guía. La causa típica es un **desalineamiento** entre las bibliotecas **Qt/PyQt** dentro de Anaconda y las bibliotecas **OpenGL/GLX (Mesa)** del sistema.

---

## ✅ Solución probada (funcionó en este equipo)
> **Objetivo:** forzar a Navigator a usar la libGL del sistema y reinstalar componentes Qt dañados en `base`.

### 1) Verificar OpenGL del sistema
Instala utilidades y revisa aceleración 3D:
```bash
sudo apt update
sudo apt install -y mesa-utils libgl1-mesa-dri libglu1-mesa xwayland
glxinfo -B
```
Salida esperada (ejemplo):
```
OpenGL renderer string: Mesa Intel(R) UHD Graphics 620 (KBL GT2)
OpenGL core profile version string: 4.6 (Core Profile) Mesa 24.x
```

### 2) Lanzar Navigator **inyectando** libGL del sistema (test rápido)
```bash
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGL.so.1 ~/anaconda3/bin/anaconda-navigator
```
Si abre correctamente, puedes hacer un alias permanente:
```bash
echo "alias anaconda-navigator='LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGL.so.1 ~/anaconda3/bin/anaconda-navigator'" >> ~/.bashrc
exec bash
```

### 3) Reparar Qt/PyQt/Navigator en el entorno `base`
> Solo si el paso anterior funciona o para dejar el entorno limpio.
```bash
conda activate base
conda remove anaconda-navigator qt-main qt pyqt -y
conda install anaconda-navigator -y
```
> **Tip:** No actualices `qt`/`pyqt` por separado; actualiza Navigator completo:
```bash
conda update anaconda-navigator -y
```

---

## Alternativas (según sesión gráfica)

### A) Si usas Wayland (GNOME)
1. Instala soporte de Qt para Wayland:
   ```bash
   sudo apt install -y qtwayland5 libqt5waylandclient5 libqt5waylandcompositor5
   ```
2. Ejecuta en modo Wayland nativo:
   ```bash
   QT_QPA_PLATFORM=wayland ~/anaconda3/bin/anaconda-navigator
   ```
3. Si falla, usa XWayland (X11 sobre Wayland):
   ```bash
   env QT_QPA_PLATFORM=xcb LIBGL_ALWAYS_INDIRECT=1 ~/anaconda3/bin/anaconda-navigator
   ```

### B) Si usas Xorg (recomendado para compatibilidad)
Si aún falla en Xorg, usa el **LD_PRELOAD** (arriba) o renderizado por software como último recurso:
```bash
QT_QPA_PLATFORM=xcb LIBGL_ALWAYS_SOFTWARE=1 ~/anaconda3/bin/anaconda-navigator
```

---

## Comprobaciones útiles
- Ver `PATH` de Anaconda:
  ```bash
  echo $PATH
  # Debe incluir: $HOME/anaconda3/bin y $HOME/anaconda3/condabin
  ```
- Asegurar `conda` disponible sin activar `base`:
  ```bash
  ~/anaconda3/bin/conda init bash
  conda config --set auto_activate_base false
  exec bash
  ```
- Confirmar que Navigator está instalado en `base`:
  ```bash
  conda list -n base | grep anaconda-navigator
  ```

---

## Buenas prácticas
- Mantén el **entorno base** limpio; crea entornos por proyecto:
  ```bash
  conda create -n ml python=3.11 numpy pandas scikit-learn matplotlib seaborn -y
  conda activate ml
  ```
- Evita mezclar actualizaciones parciales de `qt`/`pyqt`. Usa:
  ```bash
  conda update anaconda-navigator -y
  ```
- Respalda el inventario del entorno base:
  ```bash
  conda list -n base --export > ~/base_env_backup.txt
  ```

---

## Preguntas frecuentes
**¿Por qué aparece “Could not initialize GLX”?**  
Porque Qt intenta abrir un contexto OpenGL vía GLX, pero las bibliotecas dentro de Anaconda no coinciden con las del sistema (Mesa), o el plugin de plataforma (Wayland/X11) no carga adecuadamente.

**¿Por qué `QT_QPA_PLATFORM=wayland` falla?**  
Faltan los paquetes de Qt Wayland en el sistema. Instálalos con `qtwayland5` y prueba de nuevo.

**¿Puedo usar Navigator sin activar `base`?**  
Sí. Agrega `$HOME/anaconda3/bin` a tu PATH y (opcionalmente) crea el alias con `LD_PRELOAD` para evitar conflictos de GLX.

---

## Apéndice: comandos rápidos
```bash
# 1) Diagnóstico OpenGL
sudo apt update && sudo apt install -y mesa-utils libgl1-mesa-dri libglu1-mesa xwayland
glxinfo -B

# 2) Arranque “salvavidas”
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGL.so.1 ~/anaconda3/bin/anaconda-navigator

# 3) Alias permanente
echo "alias anaconda-navigator='LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGL.so.1 ~/anaconda3/bin/anaconda-navigator'" >> ~/.bashrc
exec bash

# 4) Reparación en base
conda activate base
conda remove anaconda-navigator qt-main qt pyqt -y
conda install anaconda-navigator -y

# 5) Wayland (opciones)
sudo apt install -y qtwayland5 libqt5waylandclient5 libqt5waylandcompositor5
QT_QPA_PLATFORM=wayland ~/anaconda3/bin/anaconda-navigator
env QT_QPA_PLATFORM=xcb LIBGL_ALWAYS_INDIRECT=1 ~/anaconda3/bin/anaconda-navigator

# 6) Xorg con software rendering (último recurso)
QT_QPA_PLATFORM=xcb LIBGL_ALWAYS_SOFTWARE=1 ~/anaconda3/bin/anaconda-navigator
```

---

**Autor:** Brayan Tebelán · *Notas de trabajo – Ciencia de Datos / IA / ML*
