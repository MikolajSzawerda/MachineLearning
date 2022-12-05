# Algorytm SVM
## Mikołaj Szawerda 318731

# Opis polecenia

Zadanie polega na zaimplementowaniu algorytmu SVM i zbadaniu działania na przykładzie zbioru danych Wine Quality Data Set. Zadaniem algorytmu jest określenie na podstawie podanych właściowości fizykochemicznych wina rodzaju (czerwony/biały) wina - klasyfikacja binarna.

SVM polega na wyznaczeniu linii, która jak najlepiej separuje obie klasy - równoważnie wyznaczenie jak największego obszaru separującego wektory różnych klas. Ponieważ nie każdy zbiór danych jest liniowo separowalny do algorytmu należy zastosować dodatkowe kroki zwiększające jego skuteczność:
- dodanie marginesu - linia nie musi separować od siebie dokładnie wszystkich reprezentatnów danych klas
- zastosowanie "sztuczki jądrowej" - użycie funkcji jądrowej, która pozwala policzyć iloczyn skalarny dwóch wektorów w przestrzeni wyznaczanej przez funkcję jądrową - praktycznie, pozwala to nadać dowolny kształt linii separującej

Niech:

$\hat{f}(x)=w^Tx-b$ - postać prostej, która najlepiej separuje dwie klasy

$y_i = \left\{\begin{matrix}
-1 & \hat{f}(x_i) \leqslant  0 \\
 1 & \hat{f}(x_i) > 0
\end{matrix}\right.$ - funkcja decyzyjna, o przynależności do klasy

$k(u, v)$ - przekształcenie jądrowe


Zadaniem algorytmu jest wyznacznie $w$ i $b$, a ponieważ algorytm ma mieć możliwość stosowania różnych funkcji jądrowych, program będzie realizował algorytm zapisany w postaci dualnej, gdzie:

$\hat{w}=\sum_{i}^{N}\alpha_ix_iy_i$

$\hat{b}=median(\left\{b_i:x_n \in X_n \wedge b_i=|y_n-k(\hat{w}, x_n)|\right\})$, gdzie $X_n$ - zbiór wektorów wspierających

$a_{1,...,N}=arg \space min_{\alpha}(\frac{1}{2}\sum_{i}^{N}\sum_{j}^{N}y_iy_j\alpha_i\alpha_jk(x_i,x_j)-\sum_{i}^{N}\alpha_i)$

Przy ograniczeniach: $\left\{\begin{matrix} \sum_{i}^{N}y_i\alpha_i=0, \\ (\forall_{i}=1,...,N) \space 0 \leqslant \alpha_i \leqslant C \end{matrix}\right.$


Hiperparametrami algorytmu są więc:

- $C$ - współczynnik kosztu - mnożnik kary za użycie rozluźnienia

- $k(u, v)$ - przekształcenie jądrowe

- $parametry \space k(u, v)$

# Planowane eksperymenty numeryczne

- W celu oceny konieczności zastosowania normalizacji i standaryzacji przedstawię histogramy cech

- Do oceny wpływu hiperparametrów przedstawię macierz pomyłek, oraz wykresy prezentujące TPR i FPR

- algorytm wywołam dla dwóch funkcji jądrowych:
  - $k(u, v)=u^Tv$
  - $k(u, v)=exp(\frac{-\left\|u-x\right\|^2}{2\sigma^2})$


# Wyniki
# Wnioski