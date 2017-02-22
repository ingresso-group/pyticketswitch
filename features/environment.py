def before_all(context):
    context.url = context.config.userdata.get('url', 'https://api.ticketswitch.com')
    context.config.setup_logging()


def after_tag(context, tag):
    if tag == 'dirty':
        clean_up_pending_transactions(context)


def clean_up_pending_transactions(context):

    if not hasattr(context, 'transaction_uuid'):
        return

    status = context.client.get_status(context.transaction_uuid)

    if not status:
        return

    if status.status == 'reserved':
        context.client.release_reservation(context.transaction_uuid)
        return

    if status.status == 'attempting':
        next_token = context.transaction_uuid + '99'
        context.client.next_callout(
            context.this_token,
            next_token,
            {'is_tsw_callout_timeout_callback': 1}
        )
        return
