import json, os, pyperclip as pc, sys

def notebook_to_string(notebook_path):
    """
    Convierte un Jupyter Notebook (.ipynb) a string con todo su contenido.
    
    Parámetros:
    notebook_path (str): Ruta al archivo .ipynb
    
    Retorna:
    str: Contenido completo del notebook como string
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        pc.copy(str(notebook))
        
    
    except FileNotFoundError:
        return f"Error: Archivo no encontrado en {notebook_path}"
    except json.JSONDecodeError:
        return f"Error: El archivo {notebook_path} no es un notebook válido"
    except Exception as e:
        return f"Error inesperado: {str(e)}"

# Ejemplo de uso:
if __name__ == "__main__":
    os.system('clear')

    args = sys.argv
    if   '--fase1' in args: book = 'fase_a.ipynb'
    elif '--fase2' in args: book = 'fase_b.ipynb'
    elif '--fase3' in args: book = 'fase_c.ipynb'
    elif '--fase4' in args: book = 'fase_d.ipynb'
        
    notebook_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'Notebooks',
        book
    )

    notebook_to_string(notebook_path)
    print('Done...!!!')
