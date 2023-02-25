# Naiwny Klasyfikator Bayesowski
## Mikołaj Szawerda 318731
# Opis polecenia

<div style="text-align: justify">
Zadanie polega na zaimplementowaniu nawinego klasyfikatora Bayesowskiego
oraz zbadaniu jego działania w zastosowaniu do zbioru danych Iris Data Set. Działanie klasyfikatora polega na przypoprządkowaniu prawdopodobieństwa
przynależności do klas dla danego zestawu wartości cech i wybraniu tego
o największej wartości.Prawdopodobieństwo jest wyliczane z założeniem warunkowej niezależności cech - jest
więc iloczynem prawdopodobieństw dla każdej cechy. Ponieważ cechy są typu ciągłego, oraz po przeprowadzeniu analizy rozkładu wartości,
do wyliczenia potrzebnych wartości użyję gęstości rozkładu normalnego.
</div>

Algorytm realizuje następujący wzór:

<img src="formula.svg">

gdzie

<img src="formual2.svg">,

$p(C_k)$ - prawdopodobieństwo klasy, zostało wyznaczone na podstawie liczności w zbiorze treningowym

Trening polega więc na wyznaczeniu $\mu_k$ i $\sigma^{2}_k$ dla każdej klasy i cechy z zbioru uczącego, a predykcja polega na wyliczeniu wartości dla każdej z możliwych klas i wybraniu tej najbardziej prawdopodobnej.

# Planowane eksperymenty numeryczne

Przeprowadzę klasyfikację dla zbioru testowego, dla wytrenowanego klasyfikatora odpowiednio dla
10%,...,90% dostępnych danych jako zbiór uczący, oraz zbadam osiągniętą dokładność.

<div style="page-break-after: always;"></div>

# Wyniki

<img src="plots/summary_table.png" width="600">

<img src="plots/distr.png" alt="drawing" width="800"/>

Można zauważyć, że praktycznie każda z cech ma w przybliżeniu rozkład normalny - przyjęcie gestości rozkładu normalnego ma więc swoje uzasadnienie.
Można również zauważyć, że klasa "Iris-setosa" znacząco różni się od pozostałych dwóch, co może sugerować lepsze osiągi klasyfikacji dla tej klasy.

<img src="plots/accuracy_plot.png" alt="drawing" width="600"/>

Wraz z ilością danych treningowych rośnie dokładność klasyfikacji - od stosunku $\frac{2}{3}$ danych treninogowych do testowych klasyfikator osiąga nieomylność

<img src="plots/mat_15.png" alt="drawing" width="330"/>


<img src="plots/mat_30.png" alt="drawing" width="330"/>


<img src="plots/mat_45.png" alt="drawing" width="330"/>


<img src="plots/mat_60.png" alt="drawing" width="330"/>


<img src="plots/mat_75.png" alt="drawing" width="330"/>

Pomyłki występują tylko pomiędzy klasami "Iris-virginica" i "Iris-versicolor" - co można było przewidzieć na podstawie wartości średniej i wariancji cech

<img src="plots/mat_90.png" alt="drawing" width="330"/>


<img src="plots/mat_105.png" alt="drawing" width="330"/>


<img src="plots/mat_120.png" alt="drawing" width="330"/>


<img src="plots/mat_135.png" alt="drawing" width="330"/>


<img src="plots/time_plot.png" alt="drawing" width="330"/>

Spadek czasu wykonania wraz z ilością danych treningowych wynika z wzrostu ilości danych testowych. Można zauważyć liniowy charakter algorytmu.

<div style="page-break-after: always;"></div>


# Wnioski

Naiwny klasyfikator Bayesowski dla zadanego zbioru
danych osiągnął prawidłowe rezultaty. Należy zwrócić uwagę na potrzebną ilość danych do rozpoczęcia zwracania przez algorytm pożądanych rezultatów - już dla zbioru 15 przykładów algorytm osiągnął 93% dokładność. Fakt ten można wytłumaczyć normalnym rozkładem wartości cech, przez co wyliczone przybliżone prawdopodobieństwa przynależności były bliskie wartościom teoretycznym.

Przypadki w których algorytm dokonywał błędnej klasyfikacji są związane z podobnym rozkładem cech pomiędzy klasami - jednakże w raz z odpowiednią ilością danych błąd ten w najlepszych próbach osiągnął 0.

Złożoność czasowa algorytmu jest liniowa, natomiast w czasie wykonania algorytm potrzebuje tylko tablicy wartości średniej i wariancji dla każdej kombinacji klasa-cecha

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
<script type="text/x-mathjax-config"> MathJax.Hub.Config({ tex2jax: {inlineMath: [['$', '$']]}, messageStyle: "none" });</script>