import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.control.Tooltip;
import javafx.scene.effect.DropShadow;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class miPantalla extends Application {

    @Override
    public void start(Stage stage) {

        // aqui comienza lógicamente la pantalla
        Label label = new Label("Ingrese su nombre:");

        // un texto
        TextField campoTexto = new TextField();

        // boton
        Button boton = new Button("Aceptar");
        
        Tooltip tooltip = new Tooltip("Pulsa y callate");
        boton.setTooltip(tooltip);

        DropShadow dropShadow = new DropShadow();
        boton.setEffect(dropShadow);

        boton.setOnMouseEntered(e -> boton.setStyle("-fx-background-color:#ff0000"));
        boton.setOnMouseExited(e -> boton.setStyle("-fx-background-color:#ffffff"));

        boton.setOnAction(e -> {
            String nombre = campoTexto.getText();
            System.out.println(nombre);
        });
        VBox layout = new VBox(10);
        layout.getChildren().addAll(label, campoTexto, boton);

        // crear escena
        Scene escena = new Scene(layout, 300, 200);

        stage.setScene(escena);
        stage.setTitle("Mi Pantalla");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
