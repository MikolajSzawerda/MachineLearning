# Zadanie 1 Gradient Prosty

## Mikołaj Szawerda 318731

---

## Opis zaimplementowanego algorytmu

<div style="text-align: justify">
Celem zadania było zaimplementowanie algorytmu gradientu prostego - służącego do (sub)optymalizowania zadanych funkcji matematycznych wielu zmiennych. Algorytm polega na obliczaniu wartości gradientu w zadanym punkcie - a więc kierunku wzrostu wartości funkcji - i "przejściu" do kolejnego punktu w kierunku przeciwnym do gradientu o wartość iloczynu gradientu i parametru kroku. Kluczowym jest więc odpowiednie dobranie kroku. W mojej implementacji znajdują się dwa rozwiązania - z góry ustalony krok losowany z zadanego przedziału(potencjalnie można uruchomić program dla paru wartości z przedziału) i krok dynamiczny, zmieniający się w każdej iteracji, wyszukiwany przez - "Backtrack line search". Ponieważ wybór punktu ma również ogromne znaczenie na wyniki gradientu prostego, program można uruchomić dla wielu punktów, losowanych z podanej dziedziny. Jako warunek stopu przyjąłem maksymalną ilość iteracji(n=1000), lub brak wystarczająco dużej poprawy/wartość gradientu, lub rozbieżność funkcji.

</div>


### Backtrack line search

Polega na iteracyjnym zmniejszaniu potencjalnego kroku w danej iteracji, aż do osiągnięcia zadowalającej optymalizacji z bieżącego miejsca.


## Planowane eksperymenty numeryczne

- Uruchomienie obu algorytmów dla zadanego punktu/kroku
- Uruchomienie obu algorytmów dla wielu kroków i punktów
- Uruchomienie obu algorytmów dla funkcji dwóch zmiennych w losowym punkcie i na "płaskim terenie"

W każdym eksperymencie program dokonuje zapisu obecnego obliczanego punktu, wartości funkcji w punkcie i iteracji, po za tym program mierzy czas wykonania.

Dwa pierwsze eksperymenty zostały uruchomione na proponowanej funkcji:

$q(x)=\sum_{i=1}^{n} \alpha^{\frac{i-1}{n-1}} x_{i}^{2}, x\in [-100,100]^{n}\subset \mathbb{R}^{n}, n=10$

Trzeci dla:

$q(x, y)=(1-x^{2}+y^{3})e^{-(x^{2}+y^{2})}$

<div style="page-break-after: always;"></div>

## Wyniki

## Wywołanie dla zadanego kroku i punktu

Etykieta w przypadku Fixed step stanowi przyjęty krok i odległość punktu startowego od Punktu X=0 - odpowiednio dla Backtrack step

#### α=1
<img src="../results/one_run/Fixed_step_1.png" alt="drawing" width="320"/>
<img src="../results/one_run/Backtrack_step_1.png" alt="drawing" width="320"/>

<img src="../results/one_run/times_1.png" alt="drawing" width="250"/>

#### α=10
<img src="../results/one_run/Fixed_step_10.png" alt="drawing" width="320"/>
<img src="../results/one_run/Backtrack_step_10.png" alt="drawing" width="320"/>
<div style="page-break-after: always;"></div>
<img src="../results/one_run/Bad_Fixed_step_10.png" alt="drawing" width="320"/>
<img src="../results/one_run/times_10.png" alt="drawing" width="250"/>


#### α=100

<img src="../results/one_run/Fixed_step_100.png" alt="drawing" width="320"/>
<img src="../results/one_run/Backtrack_step_100.png" alt="drawing" width="320"/>

<img src="../results/one_run/times_100.png" alt="drawing" width="250"/>

<div style="page-break-after: always;"></div>

## Wywołanie z wieloma punktami i krokami

#### α=1
<img src="../results/full_run/Fixed_step_1.png" alt="drawing" width="320"/>
<img src="../results/full_run/Backtrack_step_1.png" alt="drawing" width="320"/>

<img src="../results/full_run/times_1.png" alt="drawing" width="250"/>


#### α=10
<img src="../results/full_run/Fixed_step_10.png" alt="drawing" width="320"/>
<img src="../results/full_run/Backtrack_step_10.png" alt="drawing" width="320"/>

<img src="../results/full_run/times_10.png" alt="drawing" width="250"/>



#### α=100
<img src="../results/full_run/Fixed_step_100.png" alt="drawing" width="320"/>
<img src="../results/full_run/Backtrack_step_100.png" alt="drawing" width="320"/>

<img src="../results/full_run/times_100.png" alt="drawing" width="250"/>

<div style="page-break-after: always;"></div>

## Wywołanie dla funkcji z wieloma punktami krytycznymi i "płaskim" obszarem
<img src="../results/2d_run/Fixed_step_.png" alt="drawing" width="320"/>
<img src="../results/2d_run/Fixed_step_contour.png" alt="drawing" width="320"/>
<img src="../results/2d_run/Backtrack_step_.png" alt="drawing" width="320"/>
<img src="../results/2d_run/Backtrack_step_contour.png" alt="drawing" width="320"/>

<img src="../results/2d_run/times.png" alt="drawing" width="250"/>

<div style="page-break-after: always;"></div>

## Analiza

### Szybkość zbieżności

<div style="text-align: justify">
Przy odpowiednim dobraniu kroku, oba algorytmy w przypadku testowej funkcji osiągają zadowalającą wartość. Stały krok wymaga jednak testowania wielu potencjalnych wartości, stwarza ryzyko wpadnięcia w oscylację, lub dążenia do nieskończoności. Z wykresów można wyciągnąć wniosek o dużym wpływie wartości kroku na szybkość zbieżności - wykres stanowią proste o różnych stopniach nachylenia. Dynamiczny krok osiągał średnio zadowalającą optymalizację przy mniejszej liczbie iteracji.
</div>

### Dokładność

<div style="text-align: justify">
Algorytm gradientu pozwala uzyskać dość dokładną zoptymalizowaną wartość - wartości gradientu zmniejszające się w pobliżu minimum pozwalają w tym obszarze dokładniej zbliżać się do punktu krytycznego - wpływ jednak ponownie wywiera krok, który może być za duży i spowodować na algorytmie ciągłe przeskakiwanie minimum.  Algorytm z backtrackingiem jako jedyny stopień swobody posiada punkt startowy, co sprawia, że można go wywołać dla wielu potencjalnych punktów prowadzących do minimum, zwiększając szansę optymalizacji.
</div>

### Zachowanie w punktach krytycznych

<div style="text-align: justify">
Mankament gradientu prostego stanowi nieodpowiedni wybór punktu startowego - punkt krytyczny, lub "płaski" obszar, sprawiają, że gradient jest bliski zeru, powodując "stanie w miejscu" algorytmu. Próby zwiększania kroku nie przynoszą żadnych rezultatów.
</div>

### Szybkość wykonania

<div style="text-align: justify">
Ponieważ gradient prosty polega głównie na odejmowaniu wektorów, jest on wydajnym rozwiązaniem. Możliwości równoległego przetwarzania wielu punktów i kroków dodatkowo zmniejszają czasy wykonania. Porównując oba algorytmy, pojedyncze wywołania backtrackingu były wolniejsze, ze względu na dodatkową pętlę wykonującą się w każdej iteracji(jednakże pozwala ona zmniejszyć ilość iteracji algorytmu).
</div>

### Ograniczenia

Niewątpliwą wadą gradientu prostego są ograniczenia jakie narzuca na optymalizowany obiekt w celu skutecznej optymalizacji - ciągłość, różniczkowalność, ograniczenie, wypukłość.

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
<script type="text/x-mathjax-config"> MathJax.Hub.Config({ tex2jax: {inlineMath: [['$', '$']]}, messageStyle: "none" });</script>