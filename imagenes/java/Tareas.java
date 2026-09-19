public class Tareas {
  public static void main(String[] args) {
    if (args.length == 2 && args[0].equals("factorial")) {
      int n = Integer.parseInt(args[1]);
      long resultado = 1;
      for (int i = 2; i <= n; i++) resultado *= i;
      System.out.println(resultado);
      return;
    }
    System.err.println("Uso: factorial <entero-no-negativo>");
    System.exit(2);
  }
}
