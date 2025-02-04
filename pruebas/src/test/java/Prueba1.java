import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.assertEquals;
import org.junit.Test;

import com.example.Main;

public class Prueba1 {
    
    @Test
    public void probarSuma() {
        assertEquals(2,Main.suma(1,1));
    }

    @Test
    public void probarPar() {
        assertEquals(true,Main.pares(2,2, false));
    }

    @Test
    public void testSumarValoresPares() {
        List<Integer> numeros = Arrays.asList(1, 2, 3, 4, 5, 6);
        int resultado = Main.sumarValoresPares(numeros);
        assertEquals(12, resultado); 
    }

    @Test
    public void testNombresMayusculas() {
        List<String> nombres = Arrays.asList("juan", "maria", "pedro");
        String resultado = Main.nombresMayusculas(nombres);
        assertEquals("PEDRO", resultado);
    }
 
}