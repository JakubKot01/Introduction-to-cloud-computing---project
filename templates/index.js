// Dane testowe - pusta lista wydatków
var expenses = [];

// Funkcja generująca wiersze tabeli na podstawie danych o wydatkach
function renderExpensesTable() {
    var tableBody = document.getElementById('expenses-table-body');
    tableBody.innerHTML = ''; // Wyczyść poprzednią zawartość tabeli

    // Iteruj przez każdy wydatek i generuj odpowiedni wiersz tabeli
    expenses.forEach(function(expense) {
        var row = document.createElement('tr');

        var nameCell = document.createElement('td');
        nameCell.textContent = expense.name;
        row.appendChild(nameCell);

        var dateCell = document.createElement('td');
        dateCell.textContent = expense.date;
        row.appendChild(dateCell);

        var amountCell = document.createElement('td');
        amountCell.textContent = expense.amount;
        row.appendChild(amountCell);

        var categoryCell = document.createElement('td');
        categoryCell.textContent = expense.category;
        row.appendChild(categoryCell);

        var periodicityCell = document.createElement('td');
        periodicityCell.textContent = expense.periodicity;
        row.appendChild(periodicityCell);

        tableBody.appendChild(row); // Dodaj wiersz do tabeli
    });
}

// Wywołaj funkcję renderExpensesTable, aby wyświetlić początkową listę wydatków
renderExpensesTable();
