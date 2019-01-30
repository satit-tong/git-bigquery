from __future__ import print_function

from datetime import datetime

from airflow.models import Variable

from build_export_dag import build_export_dag, parse_bool

start_date = Variable.get('ethereum_export_start_date', '2015-07-30')
options_args = {
    'export_daofork_traces_option': parse_bool(Variable.get('ethereum_export_daofork_traces_option', 'True')),
    'export_genesis_traces_option': parse_bool(Variable.get('ethereum_export_genesis_traces_option', 'True')),
    'export_blocks_and_transactions_toggle': parse_bool(Variable.get('ethereum_export_blocks_and_transactions_toggle', 'True')),
    'export_receipts_and_logs_toggle': parse_bool(Variable.get('ethereum_export_receipts_and_logs_toggle', 'True')),
    'export_contracts_toggle': parse_bool(Variable.get('ethereum_export_contracts_toggle', 'True')),
    'export_tokens_toggle': parse_bool(Variable.get('ethereum_export_tokens_toggle', 'True')),
    'extract_token_transfers_toggle': parse_bool(Variable.get('ethereum_extract_token_transfers_toggle', 'True')),
    'export_traces_toggle': parse_bool(Variable.get('ethereum_export_traces_toggle', 'True'))
}

provider_uri = Variable.get('ethereum_provider_uri')
provider_uri_archival = Variable.get('ethereum_provider_uri_archival', provider_uri)
max_active_runs = int(Variable.get('ethereum_export_max_active_runs', ''))
max_active_runs = int(max_active_runs) if max_active_runs != '' else None

DAG = build_export_dag(
    dag_id='ethereum_export_dag',
    web3_provider_uri=provider_uri,
    web3_provider_uri_archival=provider_uri_archival,
    output_bucket=Variable.get('ethereum_output_bucket'),
    start_date=datetime.strptime(start_date, '%Y-%m-%d'),
    notifications_emails=Variable.get('notification_emails', ''),
    schedule_interval='0 1 * * *',
    export_max_workers=10,
    export_batch_size=10,
    max_active_runs=max_active_runs,
    **options_args
)