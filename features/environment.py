def before_all(context):
    context.url = context.config.userdata.get('url', 'https://api.ticketswitch.com')
    context.config.setup_logging()
