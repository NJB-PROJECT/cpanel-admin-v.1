from flask import Flask, render_template, request, redirect, url_for, flash
from app.config import Config
from app.utils.system_info import get_system_stats
from app.utils.apache_manager import list_domains, create_domain, toggle_domain, delete_domain
from app.utils.log_reader import get_log_content
from app.utils.ssl_manager import install_ssl

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    stats = get_system_stats()
    return render_template('dashboard.html', stats=stats)

@app.route('/domains')
def domains():
    domain_list = list_domains()
    return render_template('domains.html', domains=domain_list)

@app.route('/domains/add', methods=['POST'])
def add_domain():
    domain_name = request.form.get('domain')
    email = request.form.get('email')

    if domain_name and email:
        success, msg = create_domain(domain_name, email)
        if success:
            flash(f"Domain {domain_name} created successfully!", "success")
        else:
            flash(f"Error creating domain: {msg}", "danger")
    else:
        flash("Missing required fields", "warning")

    return redirect(url_for('domains'))

@app.route('/domains/toggle', methods=['POST'])
def toggle_domain_route():
    domain_name = request.form.get('domain')
    action = request.form.get('action') # 'enable' or 'disable'

    if domain_name and action:
        success, msg = toggle_domain(domain_name, enable=(action == 'enable'))
        if success:
            flash(msg, "success")
        else:
            flash(f"Error: {msg}", "danger")

    return redirect(url_for('domains'))

@app.route('/domains/delete', methods=['POST'])
def delete_domain_route():
    domain_name = request.form.get('domain')

    if domain_name:
        success, msg = delete_domain(domain_name)
        if success:
            flash(f"Domain {domain_name} deleted.", "success")
        else:
            flash(f"Error deleting domain: {msg}", "danger")

    return redirect(url_for('domains'))

@app.route('/logs')
def logs():
    access_log = get_log_content('access')
    error_log = get_log_content('error')
    return render_template('logs.html', access_log=access_log, error_log=error_log)

@app.route('/ssl')
def ssl_page():
    domain_list = list_domains()
    return render_template('ssl.html', domains=domain_list, output=None)

@app.route('/ssl/install', methods=['POST'])
def ssl_install():
    domain_name = request.form.get('domain')
    email = request.form.get('email')

    output = ""
    if domain_name and email:
        success, msg = install_ssl(domain_name, email)
        if success:
            flash(f"SSL Certificate installed for {domain_name}", "success")
        else:
            flash("SSL Installation encountered issues.", "warning")
        output = msg

    domain_list = list_domains()
    return render_template('ssl.html', domains=domain_list, output=output)

if __name__ == '__main__':
    # In production, use a WSGI server like Gunicorn
    # For dev/debug:
    app.run(host='0.0.0.0', port=5000, debug=True)
