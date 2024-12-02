import javafx.application.Application;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonType;
import javafx.scene.control.TextField;
import javafx.scene.text.Font;
import javafx.stage.Stage;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.VBox;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.Optional;
import java.util.Random;

public class WordleGame extends Application {
    private String wordToGuess;  // La palabra que el jugador debe adivinar
    private final int maxAttempts = 5;  // Número máximo de intentos
    private int attempt = 0;  // Contador de intentos realizados
    private int letterIndex = 0;  // Índice de la letra actual en el intento
    private StringBuilder currentGuess = new StringBuilder();  // Almacena el intento actual del jugador

    private TextField[][] guessSlots;  // Cuadrícula de campos de texto donde se muestran las letras de los intentos

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Wordle en JavaFX");

        try {
            // Cargar una palabra aleatoria desde un archivo
            wordToGuess = getRandomWordFromFile("C:\\Users\\galea\\OneDrive - Colegio Lagomar\\DAM\\Desarrollo de Interfaces\\2024-11-09\\ProyectoFX\\src\\main\\resources\\palabras.txt");
        } catch (IOException e) {
            // Si no se puede cargar el archivo, mostrar una alerta de error
            showAlert("Error", "No se pudo cargar la lista de palabras.");
            return;
        }

        // Crear el contenedor raíz de la interfaz
        VBox root = new VBox(20);
        root.setAlignment(Pos.CENTER);
        root.setStyle("-fx-background-color: #F0F0F0;");

        // Crear el contenedor para la cuadrícula de los intentos
        GridPane grid = new GridPane();
        grid.setAlignment(Pos.CENTER);
        grid.setVgap(10);
        grid.setHgap(10);

        // Inicializar la cuadrícula para los intentos
        guessSlots = new TextField[maxAttempts][5];
        for (int i = 0; i < maxAttempts; i++) {
            for (int j = 0; j < 5; j++) {
                guessSlots[i][j] = new TextField();
                guessSlots[i][j].setPrefWidth(50);
                guessSlots[i][j].setPrefHeight(50);
                guessSlots[i][j].setFont(Font.font("Arial", 20));
                guessSlots[i][j].setAlignment(Pos.CENTER);
                guessSlots[i][j].setEditable(false);  // No se puede editar directamente
                guessSlots[i][j].setStyle("-fx-background-color: #FFFFFF; -fx-border-color: #DDDDDD; -fx-border-radius: 5px;");
                grid.add(guessSlots[i][j], j, i);
            }
        }

        // Crear el contenedor para el teclado virtual
        VBox keyboardLayout = new VBox(5);
        keyboardLayout.setAlignment(Pos.CENTER);

        // Agregar las primeras dos filas de letras al teclado (QWERTYUIOP y ASDFGHJKLÑ)
        String[] qwertyRows = {
                "QWERTYUIOP",
                "ASDFGHJKLÑ"
        };
        for (String row : qwertyRows) {
            GridPane keyboardRow = createKeyboardRow(row);
            keyboardLayout.getChildren().add(keyboardRow);
        }

        // Agregar la fila de "ZXCVBNM" junto con los botones de Confirmar y Borrar
        GridPane zxRow = createKeyboardRowWithConfirmDelete("ZXCVBNM");
        keyboardLayout.getChildren().add(zxRow);

        // Agregar la cuadrícula de intentos y el teclado virtual al contenedor raíz
        root.getChildren().addAll(grid, keyboardLayout);

        // Configurar la escena y mostrarla
        Scene scene = new Scene(root, 600, 600);
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    private String getRandomWordFromFile(String filename) throws IOException {
        // Leer todas las palabras del archivo
        List<String> words = Files.readAllLines(Paths.get(filename));
        // Filtrar solo las palabras que tienen 5 letras
        words.removeIf(word -> word.length() != 5);
        Random random = new Random();
        // Seleccionar una palabra aleatoria
        return words.get(random.nextInt(words.size())).toUpperCase();
    }

    private GridPane createKeyboardRow(String row) {
        GridPane keyboardRow = new GridPane();
        keyboardRow.setAlignment(Pos.CENTER);
        keyboardRow.setHgap(5);

        // Crear botones para cada letra en la fila
        for (int col = 0; col < row.length(); col++) {
            Button letterButton = new Button(String.valueOf(row.charAt(col)));
            letterButton.setFont(Font.font("Arial", 18));
            letterButton.setStyle("-fx-background-color: #FFFFFF; -fx-border-radius: 5px; -fx-border-color: #DDDDDD;");
            letterButton.setPrefHeight(50);
            letterButton.setPrefWidth(50);
            // Acción cuando se hace clic en una letra
            letterButton.setOnAction(e -> handleLetterClick(letterButton));

            keyboardRow.add(letterButton, col, 0);

            // Cambiar el estilo cuando el mouse entra/sale sobre el botón
            letterButton.addEventHandler(MouseEvent.MOUSE_ENTERED, e -> letterButton.setStyle("-fx-background-color: #DDDDDD; -fx-border-radius: 5px; -fx-border-color: #DDDDDD;"));
            letterButton.addEventHandler(MouseEvent.MOUSE_EXITED, e -> letterButton.setStyle("-fx-background-color: #FFFFFF; -fx-border-radius: 5px; -fx-border-color: #DDDDDD;"));
        }

        return keyboardRow;
    }

    private GridPane createKeyboardRowWithConfirmDelete(String row) {
        GridPane keyboardRow = new GridPane();
        keyboardRow.setAlignment(Pos.CENTER);
        keyboardRow.setHgap(5);

        // Botón de confirmación (✔) para verificar el intento
        Button confirmButton = new Button("✔");
        confirmButton.setFont(Font.font("Arial", 18));
        confirmButton.setStyle("-fx-background-color: #4CAF50; -fx-text-fill: white;");
        confirmButton.setPrefHeight(50);
        confirmButton.setPrefWidth(77);
        // Acción cuando se hace clic en el botón de confirmación
        confirmButton.setOnAction(e -> checkGuess());
        keyboardRow.add(confirmButton, 0, 0);

        // Cambiar el estilo cuando el mouse entra/sale sobre el botón de confirmación
        confirmButton.addEventHandler(MouseEvent.MOUSE_ENTERED, e -> confirmButton.setStyle("-fx-background-color: #4A9B4E; -fx-text-fill: white;"));
        confirmButton.addEventHandler(MouseEvent.MOUSE_EXITED, e -> confirmButton.setStyle("-fx-background-color: #4CAF50; -fx-text-fill: white;"));

        // Crear botones para cada letra en la fila ZXCVBNM
        for (int col = 0; col < row.length(); col++) {
            Button letterButton = new Button(String.valueOf(row.charAt(col)));
            letterButton.setFont(Font.font("Arial", 18));
            letterButton.setStyle("-fx-background-color: #FFFFFF; -fx-border-radius: 5px; -fx-border-color: #DDDDDD;");
            letterButton.setPrefHeight(50);
            letterButton.setPrefWidth(50);
            // Acción cuando se hace clic en una letra
            letterButton.setOnAction(e -> handleLetterClick(letterButton));

            keyboardRow.add(letterButton, col + 1, 0);

            // Cambiar el estilo cuando el mouse entra/sale sobre el botón
            letterButton.addEventHandler(MouseEvent.MOUSE_ENTERED, e -> letterButton.setStyle("-fx-background-color: #DDDDDD; -fx-border-radius: 5px; -fx-border-color: #DDDDDD;"));
            letterButton.addEventHandler(MouseEvent.MOUSE_EXITED, e -> letterButton.setStyle("-fx-background-color: #FFFFFF; -fx-border-radius: 5px; -fx-border-color: #DDDDDD;"));
        }

        // Botón de borrar (⌫) para eliminar la última letra
        Button deleteButton = new Button("⌫");
        deleteButton.setFont(Font.font("Arial", 18));
        deleteButton.setStyle("-fx-background-color: #EE0A0A; -fx-text-fill: white;");
        deleteButton.setPrefHeight(50);
        deleteButton.setPrefWidth(77);
        // Acción cuando se hace clic en el botón de borrar
        deleteButton.setOnAction(e -> handleDeleteClick());
        keyboardRow.add(deleteButton, row.length() + 1, 0);

        // Cambiar el estilo cuando el mouse entra/sale sobre el botón de borrar
        deleteButton.addEventHandler(MouseEvent.MOUSE_ENTERED, e -> deleteButton.setStyle("-fx-background-color: #CF0B0B; -fx-text-fill: white;"));
        deleteButton.addEventHandler(MouseEvent.MOUSE_EXITED, e -> deleteButton.setStyle("-fx-background-color: #EE0A0A; -fx-text-fill: white;"));

        return keyboardRow;
    }

    private void handleLetterClick(Button letterButton) {
        // Agregar la letra seleccionada al intento actual si no se han alcanzado las 5 letras
        if (currentGuess.length() < 5) {
            currentGuess.append(letterButton.getText());
            guessSlots[attempt][letterIndex].setText(letterButton.getText());
            letterIndex++;
        }
    }

    private void handleDeleteClick() {
        // Eliminar la última letra del intento actual si hay alguna
        if (currentGuess.length() > 0) {
            currentGuess.setLength(currentGuess.length() - 1);
            letterIndex--;
            guessSlots[attempt][letterIndex].setText("");
        }
    }

    private void guessFeedback(String guess) {
        // Proporciona retroalimentación sobre el intento actual comparándolo con la palabra a adivinar
        boolean[] checked = new boolean[5];  // Para verificar qué letras ya han sido procesadas
        int[] letterCount = new int[26];  // Contador de letras en la palabra correcta

        // Contar las letras de la palabra a adivinar
        for (int i = 0; i < 5; i++) {
            letterCount[wordToGuess.charAt(i) - 'A']++;
        }

        // Verificar las letras correctas (letra y posición correctas)
        for (int i = 0; i < 5; i++) {
            if (guess.charAt(i) == wordToGuess.charAt(i)) {
                guessSlots[attempt][i].setStyle("-fx-background-color: #4CAF50; -fx-text-fill: white;");  // Verde
                checked[i] = true;
                letterCount[guess.charAt(i) - 'A']--;
            }
        }

        // Verificar las letras que están en la palabra pero en una posición incorrecta
        for (int i = 0; i < 5; i++) {
            if (!checked[i]) {
                char letter = guess.charAt(i);
                if (wordToGuess.contains(String.valueOf(letter)) && letterCount[letter - 'A'] > 0) {
                    guessSlots[attempt][i].setStyle("-fx-background-color: #FFB10B; -fx-text-fill: white;");  // Amarillo
                    letterCount[letter - 'A']--;
                } else {
                    guessSlots[attempt][i].setStyle("-fx-background-color: #B0B0B0; -fx-text-fill: white;");  // Gris
                }
            }
        }
    }

    private void checkGuess() {
        // Verificar si el intento tiene 5 letras
        if (currentGuess.length() != 5) {
            // Mostrar una alerta si el intento no tiene 5 letras
            Alert alert = new Alert(Alert.AlertType.INFORMATION);
            alert.setTitle("Error");
            alert.setHeaderText(null);
            alert.setContentText("Por favor ingresa una palabra de 5 letras.");
            alert.showAndWait();
            return;
        }

        String guess = currentGuess.toString();
        guessFeedback(guess);

        // Verificar si el intento es correcto
        if (guess.equals(wordToGuess)) {
            showAlert("¡Felicidades!", "¡Has adivinado la palabra!");
        } else if (++attempt == maxAttempts) {
            // Si se agotaron los intentos, mostrar la palabra correcta
            showAlert("Fin del Juego", "Has agotado tus intentos. La palabra era: " + wordToGuess);
        } else {
            // Limpiar el intento actual y continuar con el siguiente
            currentGuess.setLength(0);
            letterIndex = 0;
        }
    }

    private void showAlert(String title, String message) {
        // Mostrar una alerta con opciones para reiniciar o salir
        Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message + "\n¿Quieres jugar otra vez?");

        ButtonType yesButton = new ButtonType("Sí");
        ButtonType noButton = new ButtonType("No");
        alert.getButtonTypes().setAll(yesButton, noButton);

        Optional<ButtonType> result = alert.showAndWait();
        if (result.isPresent() && result.get() == noButton) {
            exitGame();
        } else {
            resetGame();
        }
    }

    private void exitGame() {
        // Salir del juego
        System.exit(0);
    }

    private void resetGame() {
        // Reiniciar el juego, eligiendo una nueva palabra
        try {
            wordToGuess = getRandomWordFromFile("C:\\Users\\galea\\OneDrive - Colegio Lagomar\\DAM\\Desarrollo de Interfaces\\2024-11-09\\ProyectoFX\\src\\main\\resources\\palabras.txt");
        } catch (IOException e) {
            showAlert("Error", "No se pudo cargar la lista de palabras.");
        }

        // Reiniciar los intentos y limpiar la cuadrícula
        attempt = 0;
        letterIndex = 0;
        currentGuess.setLength(0);

        for (int i = 0; i < maxAttempts; i++) {
            for (int j = 0; j < 5; j++) {
                guessSlots[i][j].setText("");
                guessSlots[i][j].setStyle("-fx-background-color: #FFFFFF; -fx-border-color: #DDDDDD; -fx-border-radius: 5px;");
            }
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
