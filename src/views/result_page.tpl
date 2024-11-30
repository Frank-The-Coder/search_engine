<!doctype html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Search Result</title>
        <link rel="stylesheet" href="/static/css/style.css" />
    </head>

    <body>
        % include('header.tpl')

        <!-- Main Content Container -->
        <div class="main-container">
            <h2>Search Results for "{{ user_query }}"</h2>

            % if url_results: 
                % for url in url_results:
                    <a href="{{ url }}">{{ url }}</a>
                % end 
            % else: 
                No URL is found. 
                % if corrected_query:
                    <p>Did you mean: <a href="/search?keywords={{ corrected_query }}">{{ corrected_query }}</a>?</p>
                % end
            % end
            <br />
            <!-- Pagination Buttons -->
            <div class="pagination">
                % if current_page > 1:
                    <a href="/search?keywords={{ user_query }}&page={{ current_page - 1 }}" class="pagination-button">Previous</a>
                % end

                <span>Page {{ current_page }} of {{ total_pages }}</span>

                % if current_page < total_pages:
                    <a href="/search?keywords={{ user_query }}&page={{ current_page + 1 }}" class="pagination-button">Next</a>
                % end
            </div>
            <br />
            <a href="/" class="back-button">Go Back</a>
        </div>
    </body>
</html>
