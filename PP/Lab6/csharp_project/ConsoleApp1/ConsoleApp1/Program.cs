using System.Diagnostics;
using System.Text.Json;

namespace ConsoleApp1;

public class ModelResult
{
    public string status { get; set; }
    public string prediction { get; set; }
}

class Program
{
    static void Main(string[] args)
    {
        Console.Write("Введите вес: ");
        string weight = Console.ReadLine();
        Console.Write("Введите рост: ");
        string height = Console.ReadLine();

        string projectRoot = Directory.GetParent(AppContext.BaseDirectory)?.Parent?.Parent?.Parent?.Parent?.Parent?.Parent?.FullName;
        string scriptPath = Path.Combine(projectRoot, "model_pipeline.py");

        string jsonInput = $"{{\"weight\": \"{weight}\", \"height\": \"{height}\"}}";
        string escapedJson = jsonInput.Replace("\"", "\\\"");
        
        ProcessStartInfo start = new()
        {
            FileName = "python3",
            Arguments = $"\"{scriptPath}\" \"{escapedJson}\"",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true
        };

        try
        {
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string stderr = process.StandardError.ReadToEnd();
                    string result = reader.ReadToEnd();

                    if (!string.IsNullOrEmpty(stderr))
                        Console.WriteLine("Ошибка Python: " + stderr);

                    Console.WriteLine("Ответ от модели:");
                    var data = JsonSerializer.Deserialize<ModelResult>(result);
                    Console.WriteLine($"Статус: {data.status}");
                    Console.WriteLine($"Предсказание: {data.prediction}");
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("Ошибка запуска: " + ex.Message);
        }

        Console.ReadKey();
    }
}