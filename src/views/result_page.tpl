<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Result</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>

<body>
    % include('header.tpl')

    <!-- Main Content Container -->
    <div class="main-container">
        <h2>Search Results for "{{ user_query }}"</h2>

        <!-- Results Table -->
        <table id="results">
            <thead>
                <tr>
                    <th>Word</th>
                    <th class="text_left_align">Count</th>
                </tr>
            </thead>
            <tbody>
                % for word, count in word_count.items():
                <tr>
                    <td>{{ word }}</td>
                    <td class="text_left_align">{{ count }}</td>
                </tr>
                % end
            </tbody>
        </table>

        <br>
        <a href="/" class="back-button">Go Back</a>
    </div>
</body>

</html>