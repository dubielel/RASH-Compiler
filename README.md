# Kompilator języka RASH do C

## Dane studentów
  * Kacper Cienkosz, kcienkosz@student.agh.edu.pl 
  * Miłosz Dubiel, miloszdubiel@student.agh.edu.pl
  * Krzysztof Wójcik, wojcikkrs@student.agh.edu.pl

## Założenia programu
Celem projektu jest stworzenie kompilatora własnego języka RASH do C. RASH jest językiem obiektowym, swoistym połączeniem naszym zdaniem najlepszych cech innych języków, tj. Python, Rust, Java. Ponadto, do kompilatora zostały stworzone CLI do translacji oraz kompilacji i uruchamiania programów jak również GUI do edycji i uruchamiania programów.

## Wykorzystane technologie
  * Generator parserów: ANTLRv4
  * Język akcji/implementacji: Python
  * GUI: PyQt5
  * CLI: bash

## Spis tokenów
[LanguageTestLexer](https://github.com/dubielel/RASH-Compiler/blob/v1.0.1/grammar/LanguageTestLexer.g4)

Opisuje takie składniki jak: słowa kluczowe do pętli, wyrażeń warunkowych, operatorów dostępu, klas, metod/funkcji, wyrażeń logicznych, podstawowych typów danych, notacji zapisu liczb, napisów, typu boolowskiego i wszystkich nazw stworzonych przez użytkownika, jak również znaki przypisania, operacji matematycznych, wyrażeń relacyjnych itp.

## Gramatyka przetwarzanego formatu
[LanguageTestParser](https://github.com/dubielel/RASH-Compiler/blob/v1.0.1/grammar/LanguageTestParser.g4)

Opisuje konstruowanie takich składników jak: importów, deklaracji, przypisań, wyrażeń zwracających wartość i niezwracających wartości, funkcji/metod, klas, pętli, wyrażeń warunkowych itd.

## Krótka instrukcja obsługi

### Instalacja i wymagania wstępne
Najpierw należy pobrać folder skompresowany z najnowszą wersją:

    git clone -b v1.0.1 https://github.com/dubielel/RASH-Compiler RASH-Compiler

Następnie należy utworzyć środowisko, np. za pomocą narzędzia ``pipenv``, znajdując się w katalogu głównym repozytorium:

    pipenv install

Oprócz tego, do obsługi CLI może być potrzebny ''CMake'':
  * Ubuntu i pokrewne:

        sudo apt install cmake

  * MacOS:

        subo brew install cmake


### CLI
Należy wpisać i uruchomić komendę (będąc w katalogu głównym):

    ./rash.sh [OPTIONS]

gdzie ``OPTIONS`` to:
  * ``-f [FILE]`` -- translacja kodu z pliku .rash na .c
  * ``-r [FILE]`` -- kompilacja kodu z pliku .rash przy użyciu CMake i uruchomienie programu
  * ``-h`` -- wiadomość z opisem możliwych opcji


### GUI
Aby uruchomić GUI należy wywołać komendę (będąc w katalogu głównym):

    python editor/RASHeditor.py

Spowoduje to uruchomienie aplikacji okienkowej - prostego edytora tekstowego z możliwością przeglądania drzewa plików w katalogu głównym, wpisywania kodu w języku RASH i przeprowadzenia kompilacji i uruchomienia skompilowanego programu.

W aplikacji można też otwierać i tworzyć nowe katalogi i pliki. Proces kompilacji następuje po kombinacji klawiszy ''Ctrl+R'' lub poprzez wybranie opcji ''Run'' z paska narzędzi. Wynik programu pojawi się w polu oznaczonym jako 'Terminal...'

## Przykłady
Przykładowy kod akceptowany przez kompilator:

    class ClassName {
         private var attr1: str;
    	    public var attr2: int;
    
	    public func __init__(param1: str, param2: int) -> ClassName {
	         attr1 = param1;
              attr2 = param2;
	    }
	    
	    public func testFunc() -> void {
	         var i: int = 1;
	         while (i < 10) {
                    print(i);
                    i += 1;
              }
         }
    }

    class Program {
         public static func main(args: str[]) -> void {
              var obj: ClassName = new ClassName("test", 123);
              
              // print(obj.attr1);
              print(obj.attr2);
    
              obj.testFunc();
         }
    }

Przykład z zmiennymi typu static:

    class Program {
         public static var staticVarWithAssign: int = 123;
         public static var staticVar: int;
    
         public static func staticTestFunc() -> int {
              staticVarWithAssign += 1;
         }
    
         public static func main(args: str[]) -> void { 	
              staticVar = 321;
              print(staticVar);
    
              print(staticVarWithAssign);
              staticTestFunc();
              print(staticVarWithAssign);
         }
    }

Przykład z dziedziczeniem:

    class ClassName2 {
         private var attr1: str;
         public var attr2: int;
    
         public func __init__(param1: str, param2: int) -> ClassName2 {
              attr1 = param1;
              attr2 = param2;
              print(attr2);
         }
    
         public func testFunc() -> void {
              var i: int = 1;
              while (i < 10) {
                    print(i);
                    i += 1;
              }
         }
    
         public func overrideTestFunc() -> void {
              print("override classname2");
         }
    }
    
    class ClassName3 (ClassName2) {
         private var attr3: float;
    
         public func __init__(param1: str, param2: int, param3: float) -> ClassName3 {
              super.__init__(param1, param2);
              attr3 = param3;
         }
    
         public func someFunc() -> void {
              print(attr3);
         }
    
         public func overrideTestFunc() -> void {
              print("override classname3");
         }
    }
    
    class Program {
         public static func main(args: str[]) -> void {
              var obj2: ClassName2 = new ClassName2("test", 456);
              obj2.testFunc();
              obj2.overrideTestFunc();
    
              var obj3: ClassName3 = new ClassName3("test", 123, 21.37);
              obj3.someFunc();
              obj3.testFunc();
              obj3.overrideTestFunc();
         }
    }