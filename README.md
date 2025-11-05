# Guía de comandos de Conda y buenas prácticas (Linux/Windows)

> **Autor:** Brayan Tebelán — Notas de trabajo (Ciencia de Datos / IA / ML)  
> **Última actualización:** 2025-11-05

---

## 1) Conceptos clave
- **Conda**: gestor de entornos y paquetes (Anaconda/Miniconda/Mambaforge).
- **Entorno**: carpeta aislada con su propio Python y paquetes.
- **Canales**: repositorios de paquetes (p. ej., `defaults`, `conda-forge`).
- **Solver**: motor que resuelve dependencias (`classic` o `libmamba`).

---

## 2) Instalación y actualización
### Linux
```bash
# Anaconda (full) o Miniconda (mínimo)
# Después de instalar, inicializa para tu shell:
~/anaconda3/bin/conda init bash
# Evita que (base) se active siempre
conda config --set auto_activate_base false
# Actualiza conda
conda update -n base conda -y
# (Opcional) Instala el solver rápido
conda install -n base conda-libmamba-solver -y
conda config --set solver libmamba   # o classic
```

### Windows (Anaconda Prompt)
```bat
conda init powershell
conda config --set auto_activate_base false
conda update -n base conda -y
conda install -n base conda-libmamba-solver -y
conda config --set solver libmamba  REM o classic
```

> **Nota Windows:** si Anaconda está en `C:\ProgramData\anaconda3` (instalación “All Users”),
puede requerir **Anaconda Prompt (Admin)** para actualizar base. Alternativamente, configura rutas de usuario:
```bat
conda config --add pkgs_dirs "%USERPROFILE%\conda\pkgs"
conda config --add envs_dirs "%USERPROFILE%\conda\envs"
```

---

## 3) Configuración (.condarc)
Archivo por usuario: `~/.condarc` (Linux) o `%USERPROFILE%\.condarc` (Windows).

```yaml
channels:
  - conda-forge
  - defaults
channel_priority: flexible   # strict|flexible
auto_activate_base: false
# solver: libmamba            # o classic
pkgs_dirs:
  - ~/conda/pkgs              # opcional (Linux)
envs_dirs:
  - ~/conda/envs              # opcional (Linux)
```

### Comandos útiles de config
```bash
conda config --show
conda config --show-sources
conda config --add channels conda-forge
conda config --set channel_priority flexible
conda config --set solver libmamba     # o classic
conda config --remove-key solver       # elimina la clave
```

---

## 4) Gestión de entornos
```bash
# Crear
conda create -n ml python=3.11 -y
# Crear con paquetes iniciales
conda create -n ds python=3.11 numpy pandas scikit-learn jupyterlab -y

# Activar / Desactivar
conda activate ml
conda deactivate

# Listar / info
conda env list
conda info -e

# Clonar
conda create -n ml-clone --clone ml -y

# Eliminar
conda remove -n ml --all -y
```

### Ubicación de entornos (recomendado)
- Linux: `~/conda/envs` (propio del usuario)
- Windows: `%USERPROFILE%\conda\envs`

Configúralo en `.condarc` para evitar permisos de administrador.

---

## 5) Gestión de paquetes
```bash
# Instalar en el entorno activo
conda install numpy pandas -y
# Instalar desde un canal específico
conda install -c conda-forge matplotlib -y
# Actualizar
conda update --all -y           # o paquetes puntuales
# Desinstalar
conda remove scikit-learn -y
# Buscar
conda search xgboost
```

### Consejos de canales
- Prioriza **conda-forge** cuando necesites paquetes recientes/compatibles en ciencia de datos.
- Evita mezclar demasiados canales para reducir conflictos.
- Si necesitas reproducibilidad, usa `channel_priority: strict` y fija versiones en `environment.yml`.

---

## 6) Exportar / Reproducir entornos
```bash
# Exportar (portátil entre OS)
conda env export --from-history > environment.yml
# Exportar completo (incluye versiones exactas y canales)
conda env export > environment.lock.yml

# Crear desde archivo
conda env create -f environment.yml
# Actualizar un entorno existente desde yml
conda env update -n ml -f environment.yml --prune
```

> **Consejo:** `--from-history` guarda solo los paquetes “declarados”; es mejor para reproducibilidad entre plataformas.  
> Para un “lockfile” exacto, usa el export completo.

---

## 7) Interoperabilidad con `pip`
```bash
# Preferir conda cuando exista el paquete
conda install fastapi -y
# Solo usar pip si el paquete no está en conda/conda-forge
pip install package-not-in-conda

# Recomendación: habilita pip dentro del entorno conda activo
python -m pip install --upgrade pip
pip list
```

**Buenas prácticas con pip:**
- Evita `sudo pip` y `pip --user` dentro de entornos conda.
- Si instalas con pip, documenta esa dependencia en tu README o en `requirements.txt` del proyecto.
- Para exportar también paquetes instalados con pip:
  ```bash
  conda env export > environment.lock.yml
  ```

---

## 8) JupyterLab / kernels por entorno
```bash
# Instalar JupyterLab en un entorno de trabajo
conda install -n ml jupyterlab -y
conda activate ml

# Registrar kernel de IPython con nombre amigable
python -m ipykernel install --user --name ml --display-name "Python (ml)"
# Eliminar kernel
jupyter kernelspec uninstall ml
```

---

## 9) Solver (classic vs libmamba)
```bash
# Ver solver actual
conda info | grep -i solver    # Linux/macOS
conda info | findstr /i solver # Windows

# Fijar solver
conda config --set solver libmamba   # o classic

# Forzar solver por comando (sesión actual)
CONDA_SOLVER=classic conda install numpy -y        # Linux
set CONDA_SOLVER=classic && conda install numpy -y # Windows (Cmd)
```

**Notas:**
- `libmamba` es mucho más rápido; requiere `conda-libmamba-solver` en **base**.
- Si ves: *“module 'libmambapy' has no attribute 'QueryFormat'”*,
  alinea versiones removiendo e instalando de nuevo `conda-libmamba-solver` (en base) o usa `classic`.

---

## 10) Limpieza y diagnóstico
```bash
# Limpiar caché de paquetes
conda clean -a -y     # (pkgs, tarballs, index)
# Comprobar salud del entorno
conda list
conda info
conda doctor          # (si está disponible en tu versión)
# Comprobar fuentes de configuración
conda config --show-sources
```

**Reparación rápida de base (si algo se corrompe en Qt/Navigator):**
```bash
conda activate base
conda remove anaconda-navigator qt-main qt pyqt -y
conda install anaconda-navigator -y
```

---

## 11) Anaconda Navigator (GUI)
```bash
# Linux (si no inicia por GLX en Intel):
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGL.so.1 anaconda-navigator
# O Wayland nativo (si tienes qtwayland5):
QT_QPA_PLATFORM=wayland anaconda-navigator
```
Windows: lanzar desde menú Inicio o `anaconda-navigator` en Anaconda Prompt.

---

## 12) Buenas prácticas (checklist)
- [ ] **No** trabajes en `base`; crea entornos por proyecto.
- [ ] Fija versiones mínimas de Python y librerías críticas (`python=3.11`, `pandas>=2.2`).
- [ ] Mantén un `environment.yml` por proyecto (exporta con `--from-history`).
- [ ] Usa **conda-forge** como canal principal si necesitas paquetes recientes/compatibles.
- [ ] Evita mezclar demasiados canales simultáneamente.
- [ ] Prefiere `libmamba` (siempre que base tenga `conda-libmamba-solver` sano).
- [ ] Documenta paquetes instalados con `pip` y justifica por qué no están en conda.
- [ ] Automatiza la creación de entornos en CI/CD con el `environment.yml`.
- [ ] Respeta **rutas de usuario** para `envs_dirs` y `pkgs_dirs` (evita permisos de admin).
- [ ] Respalda tu entorno base: `conda list -n base --export`.

---

## 13) Snippets rápidos
```bash
# Nuevo entorno DS “completo” (conda-forge primero)
conda create -n ds -c conda-forge python=3.11 numpy pandas scipy scikit-learn matplotlib seaborn jupyterlab ipykernel -y

# Registrar kernel
conda activate ds
python -m ipykernel install --user --name ds --display-name "Python (ds)"

# Exportar e importar
conda env export --from-history > environment.yml
conda env create -f environment.yml
```

---

## 14) Problemas comunes y soluciones breves
- **EnvironmentNotWritableError (Windows, `C:\ProgramData\anaconda3`)**  
  → Usa Anaconda Prompt como **Administrador**, o define `envs_dirs` y `pkgs_dirs` en tu perfil de usuario (ver sección 2).

- **`Could not initialize GLX` (Linux con Intel)**  
  → Usa `LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGL.so.1 anaconda-navigator` o reinstala Qt/Navigator (ver sección 10/11).

- **`libmambapy`/`QueryFormat`**  
  → `conda config --set solver classic`; luego elimina `conda-libmamba-solver` y reinstálalo en **base**; actualiza `conda`.

- **`conda: command not found` tras instalar**  
  → `~/anaconda3/bin/conda init bash` y `exec bash` (Linux) o `conda init powershell` (Windows).

---

### Fin
Esta guía resume los comandos esenciales y las prácticas recomendadas para flujos de trabajo reproducibles y estables con Conda en ciencia de datos/ML.