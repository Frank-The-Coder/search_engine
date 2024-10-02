<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Result</title>
    <link rel="stylesheet" type="text/css" href="/static/css/style.css">
</head>

<body>
    <h2>Search for "{{ user_query }}"</h2>
    <table id="result">
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
    <a href="/">Go Back</a>
</body>

</html>