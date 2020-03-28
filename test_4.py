import dash
import dash_html_components as html


class CustomDash(dash.Dash):
    def interpolate_index(self, **kwargs):
        # Inspect the arguments by printing them
        print(kwargs)
        return '''
        <!DOCTYPE html>
        <html>
            <table class="simpletable">
                <caption>OLS Regression Results</caption>
            </table>
        </html>
        '''

app = CustomDash()

app.layout = html.Div('Simple Dash App')

if __name__ == '__main__':
    app.run_server(debug=True)