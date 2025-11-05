# Instalación de Anaconda

Anaconda es una distribución de Python enfocada en ciencia de datos, inteligencia artificial y análisis científico, que incluye Python + cientos de librerías preinstaladas + un gestor de entornos y paquetes propio llamado Conda.

1. Descargar el archivo oficial de [Anaconda](https://www.anaconda.com/)
2. Ejecutar el archivo descargado.
	1. ```
	   bash Anaconda3-2025.06-0-Linux-x86_64.sh
	   ```
3. Al finalizar la instalción ejecutar el siguiente comando para evitar que conda ejecute su entorno cada vez que se abre la terminal.
	1. ```
	   ~/anaconda3/bin/conda init bash
		conda config --set auto_activate_base false
	   ```
	   >Si no se reconoce el comando `conda` reiniciar la terminal y ejecutar de nuevo.
4. Instalar Anaconda Navigator (Opcional)
	1. ```
	   conda install anaconda-navigator -y
	   ```
	2. ```
	   #Ejecutar Anaconda Navigator
	   anaconda-navigator
	   ```
	   > Si te aparece un error de entorno gráfico (por ejemplo en servidores o WSL), asegúrate de tener un entorno de escritorio activo o ejecutarlo con soporte de X11 o Wayland (no funciona en modo consola pura).