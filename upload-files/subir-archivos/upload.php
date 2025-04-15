<?php
// Definir la carpeta donde se guardarán los archivos
$uploadDir = '../../uploads/';

// Crear la carpeta si no existe
if (!is_dir($uploadDir)) {
	mkdir($uploadDir, 0777, true);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	
	if (isset($_FILES['file'])) {

		$file = $_FILES['file'];
		
		// Nombre y ruta completa del archivo a guardar
		$filePath = $uploadDir . basename($file['name']);

		// Mover el archivo a la carpeta
		if (move_uploaded_file($file['tmp_name'], $filePath)) {
			echo "Archivo subido exitosamente.";
		} else {
			echo "Error al subir el archivo.";
		}
	} else {
		echo "No se recibió ningún archivo.";
	}
} else {
	echo "Método no permitido.";
}
?>
