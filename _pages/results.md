---
title: Results
---

<table id="results-table">
    <thead>
        <tr>
            <th>Date</th>
            <th>Type</th>
            <th>Location</th>
            <th>Game Type</th>
            <th>Level Guarantee</th>
            <th>Duration (min)</th>
            <th>Cash In</th>
            <th>Cash Out</th>
            <th>Net</th>
            <th>Place</th>
            <th>Bullets</th>
        </tr>
    </thead>
    <tbody>
        {% for tournament in site.data.results %}
        <tr>
            <td>{{ tournament.date }}</td>
            <td>{{ tournament.type }}</td>
            <td>{{ tournament.location }}</td>
            <td>{{ tournament.game_type }}</td>
            <td>{{ tournament.level_guarantee }}</td>
            <td>{{ tournament.duration_min }}</td>
            <td>{{ tournament.cash_in }}</td>
            <td>{{ tournament.cash_out }}</td>
            <td>{{ tournament.net }}</td>
            <td>{{ tournament.place }}</td>
            <td>{{ tournament.bullets }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<!-- Include jQuery and DataTables.js -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
<link rel="stylesheet" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css">

<script>
    $(document).ready(function() {
        $('#results-table').DataTable();
    });
</script>

