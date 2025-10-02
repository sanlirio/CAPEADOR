import net.sf.jasperreports.engine.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;
import org.json.*;

public class ReportGenerator {

    public static void main(String[] args) {
        if (args.length < 3) {
            System.out.println("Usage: java ReportGenerator <input.jrxml> <output.jasper> <output.pdf>");
            return;
        }

        String jrxmlFile = args[0];
        String jasperFile = args[1];
        String pdfFile = args[2];
		String param = args[3];
		
		JSONArray jparam = new JSONArray(param);
		
		System.out.println(jparam);
		
        // Database connection details
        String url = "jdbc:postgresql://10.30.2.106:5432/larco_data_data_mesh";
        String username = "forms_descarga_user01";
        String password = "L@rco@!2025@";

        try (Connection conn = DriverManager.getConnection(url, username, password)) {
            // Step 1: Compile the JRXML file to a Jasper file
            System.out.println("Compiling report...");
            JasperCompileManager.compileReportToFile(jrxmlFile, jasperFile);
            System.out.println("Report compiled successfully to: " + jasperFile);

            // Step 2: Create an empty parameters map
            Map<String, Object> parameters = new HashMap<>();
			
			        // Iterate over the JSONArray
			for (int i = 0; i < jparam.length(); i++) {
				// Get the JSONObject at the current index
				JSONObject jsonObject = jparam.getJSONObject(i);

				// Loop through each key in the JSONObject
				for (String key : jsonObject.keySet()) {
					// Get the value corresponding to the key
					Object value = jsonObject.get(key);

					// Assign key and value to variables (if needed)
					parameters.put(key, value);

				}
			}

            // Step 3: Fill the report with the MySQL database connection
            System.out.println("Filling report...");
            System.out.println(jasperFile);
            System.out.println(conn);
            System.out.println(parameters);
            JasperPrint jasperPrint = JasperFillManager.fillReport(jasperFile, parameters, conn);

            // Step 4: Export the filled report to a PDF file
            System.out.println("Exporting report to PDF...");
            JasperExportManager.exportReportToPdfFile(jasperPrint, pdfFile);
            System.out.println("PDF generated successfully at: " + pdfFile);

        } catch (JRException | SQLException e) {
            e.printStackTrace();
        }
    }
}



