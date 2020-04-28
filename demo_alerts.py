import requests, json

#REST API for VictorOps Instance
url = 'REST API Endpoint'

headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "53a0f7a7-c897-4332-acfd-ec4b88614bb2"
    }

#random number generator for entity_id

def post_alert(monitoring_tool):
	response = requests.request("POST", url, data=json.dumps(monitoring_tool), headers=headers)
	print(response.text)

# SignalFX
signalfx = {
			"detector": "Memory usage detector",
  			"vo_annotate.u.Detector": "https://app.YOUR_SIGNALFX_REALM.signalfx.com/#/detector/ABCDEFGHIJK/edit",
  			"detector_url": "https://app.YOUR_SIGNALFX_REALM.signalfx.com/#/detector/ABCDEFGHIJK/edit",
  			"description": "A detector which alerts when memory usage exceeeds 90% for 10 minutes",
  			"entity_display_name": "Memory has reached 90% of maximum for 10 minutes",
  			"state_message":"A detector which alerts when memory usage exceeeds 90% for 10 minutes",
  			"entity_id": "BCDEFGHIJKL",
  			"message_type":"critical",
  			"VO_MONITOR_TYPE": 4,
  			"incidentId": "BCDEFGHIJKL",
  			"eventType": "foo",
  			"rule": "Running out of memory",
  			"severity": "Minor",
  			"monitoring_tool":"signalfx",
  			"detectOnCondition": "when(A > 90, '10m')",
 	 		"detectOffCondition": "when(A < 90, '15m')",
  			"status": "ok",
  			"routing_key":"sre",
  			"statusExtended": "ok",
  			"vo_annotate.i.Graph": "https://help.victorops.com/wp-content/uploads/2019/10/sfxcrit-1.png",
  			"image_url": "https://help.victorops.com/wp-content/uploads/2019/10/sfxcrit-1.png",
  			"timestamp": "2016-11-08T19:43:30Z",
  			"vo_annotate.u.Runbook": "https://confluence.buttercupmotors.com/charging-station-canary-runbook",
  			"vo_annotate.n.Note": "lick my butt",
 	 		"runbook_url": "https://confluence.buttercupmotors.com/charging-station-canary-runbook",
  			"inputs._S1.dimensions.host": "i-346235qa",
  			"inputs._S1.dimensions.plugin": "signalfx-metadata",
  			"inputs._S1.value": 96.235234634345,
  			"inputs._S1.fragment": "data('memory.utilization')",
  			"sf_schema": 2

  			}

# Splunk Core
splunk_core = {
			"monitoring_tool":"Splunk",
			"message_type":"CRITICAL",
  			"entity_id":"Splunk",
  			"app":"search",
  			"owner":"admin",
  			"results_file":"/Applications/Splunk/var/run/splunk/dispatch/scheduler__admin__search__RMD5606e5740f6f77d6a_at_1574274300_32/results.csv.gz",
  			"results_link":"http://dwiedenheft-MBP-3EDBB:8000/app/search/@go?sid=scheduler__admin__search__RMD5606e5740f6f77d6a_at_1574274300_32",
  			"search_name":"slow query log",
  			"search_uri":"/servicesNS/nobody/search/saved/searches/slow+query+log",
  			"server_host":"dwiedenheft-MBP-3EDBB",
  			"server_uri":"https://127.0.0.1:8089",
  			"session_key":"2^noqQFljc_qRdpJeYfzgpTPqsHXvOiqnsc6gz3jA3_OeECbvhOpTIAbnb^ba04aT7W9KZ8MOO2kJiQEqGPVHXMc_o95FOIlBkxzmb^qrSs1c28rIFMyWEhWC5L2_3tG6mZ5_qL",
 		 	"sid":"scheduler__admin__search__RMD5606e5740f6f77d6a_at_1574274300_32",
  			"version":"1.0.17",
  			"view_report":"http://dwiedenheft-MBP-3EDBB:8000/app/search/@go?sid=scheduler__admin__search__RMD5606e5740f6f77d6a_at_1574274300_32",
  			"VO_ROUTING_KEYS":"sre",
  			"X-Amzn-Trace-Id":"Root=1-5dd585b1-79547de02e1dc2e6dd15d9da",
  			"X-Forwarded-For":"50.220.40.2, 172.68.34.124",
  			"X-Forwarded-Port":"443"

  			}

# Splunk ITSI
splunk_itsi = {
			  "CONTACTGROUPNAME": "devops",
			  "NOTIFICATIONTYPE": "CRITICAL",
			  "SERVICESTATE": "CRITICAL",
			  "ServiceNow_Integration": "true",
			  "VO_ALERT_RCV_TIME": "${{VO_ALERT_RCV_TIME}}",
			  "VO_ALERT_TYPE": "SERVICE",
			  "VO_MONITOR_TYPE": "4",
			  "VO_ORGANIZATION_ID": "${{VO_ORGANIZATION_ID}}",
			  "VO_ROUTING_KEYS": "devops",
			  "VO_UUID": "${{VO_UUID}}",
			  "X-Forwarded-For.0": "54.89.199.105",
			  "X-Forwarded-For.1": "162.158.79.45",
			  "X-Forwarded-Proto": "https",
			  "X-Request-Start": "t=1537966259305",
			  "alert_type": "CRITICAL",
			  "api_key": "${{_CONTACTVO_ORGANIZATION_KEY}}",
			  "app": "SA-ITOA",
			  "entity_display_name": "Customer Transaction Issue",
			  "entity_id": "Customer Transaction Issue",
			  "entity_state": "CRITICAL",
			  "message_type": "CRITICAL",
			  "monitoring_tool": "splunk-itsi",
			  "owner": "system",
			  "results_file": "/four/splunk/var/run/splunk/dispatch/1537966271.22972/sendalert_temp_results.csv.gz",
			  "results_link": "https://OD-FM-CONF-NA-i-0447c3345e1f57e65.amazonaws.com:443/app/SA-ITOA/@go?sid=1537966271.22972",
			  "routing_key": "devops",
			  "search_name": "",
			  "server_host": "OD-FM-CONF-NA-i-0447c3345e1f57e65.amazonaws.com",
			  "server_uri": "https://127.0.0.1:8089",
			  "session_key": "veH6^6pv3jBJX^tmUi^5AnNaDczrN6OGhoDNU9ydz_ZZ8U2Hus9mFO8^SWonv2w0laU6V1oX_15agNqA^y2rGDZsxO30^ZM5erRQQzm4JbWjYCGMsFtlut896_l2dPDKKf^3m^JJEyg",
			  "sid": "1537966271.22972",
			  "splunk._raw": "{&quot;alert_value&quot;:&quot;10.59&quot;,&quot;orig_rid&quot;:&quot;0&quot;,&quot;drilldown_search_earliest_offset&quot;:&quot;-300&quot;,&quot;itsi_group_assignee&quot;:&quot;unassigned&quot;,&quot;itsi_group_count&quot;:&quot;2&quot;,&quot;event_description&quot;:&quot;Database Events status was critical (Health Score=10.59) at  2018-09-26 12:46:00.000 PM&quot;,&quot;search_name&quot;:&quot;Database Events&quot;,&quot;itsi_policy_id&quot;:&quot;59723e39d912572168796776&quot;,&quot;latest_alert_level&quot;:&quot;6&quot;,&quot;severity_value&quot;:&quot;10.59&quot;,&quot;severity_label&quot;:&quot;critical&quot;,&quot;itsi_group_title&quot;:&quot;Customer Transaction Issue&quot;,&quot;time&quot;:&quot; 2018-09-26 12:46:00.000 PM&quot;,&quot;orig_raw&quot;:&quot;09/26/2018 12:46:00 +0000, search_name=service_health_monitor, search_now=1537965960.000, info_min_time=1537963260.000, info_max_time=1537965960.000, info_search_time=1537965964.919, alert_level=6, alert_severity=critical, all_service_kpi_ids=\\&qu...",
			  "splunk.itsi_group_id": "f3da1f7e-4ea2-4e8d-a8af-dd40b8019c8f",
			  "splunk.itsi_group_title": "Customer Transaction Issue",
			  "splunk.search_name": "Database Events",
			  "state_message": "Customer Transaction Issue",
			  "state_start_time": "1537966271927",
			  "timestamp": "1537966271927",
			  "view_report": "https://OD-FM-CONF-NA-i-0447c3345e1f57e65.amazonaws.com:443/app/SA-ITOA/@go?sid=1537966271.22972"

			  }

# Splunk ES
splunk_es = {
			"monitoring_tool":"Splunk Enterprise Security",
			"message_type":"CRITICAL",
  			"entity_id":"Splunk Enterprise Security Demo Alert",

  			}

# Datadog
datadog = {
  			"monitoring_tool":"Datadog",
			"message_type":"CRITICAL",
  			"entity_id":"Datadog Demo Alert",
  			"aggregation_key":"org_id:335176|metric:system.disk.in_use|monitor_id:13713035|#device:d:",
  			"dd.auto_tags.host":"VA-MAIL-1",
  			"dd.custom_tags.device":"d:",
  			"dd.custom_tags.email_server":"va-mail-1",
  			"dd.custom_tags.host":"va-mail-1",
  			"dd.custom_tags.jleone":"live",
  			"dd.custom_tags.mail":"va-1",
  			"dd.custom_tags.mail_server":"va-mail-1",
  			"dd.custom_tags.monitor":"null",
  			"dd.custom_tags.ow":"va-mail-1.victorops.net",
  			"dd.tags.device":"d:",
  			"dd.tags.email_server":"va-mail-1",
  			"dd.tags.host":"va-mail-1",
  			"dd.tags.jleone":"live",
  			"dd.tags.mail":"va-1",
  			"dd.tags.mail_server":"va-mail-1",
  			"dd.tags.monitor":"null",
  			"dd.tags.ow":"va-mail-1.victorops.net",
  			"event_id":5173497854976151764,
  			"event_type":"query_alert_monitor",
  			"event_url":"https://app.datadoghq.com/event/event?id=5173497854976151764",
  			"is_vo_ack":1,
  			"last_updated":1572627367000,

  			}

def main():
	while True:
		userIn = int(input('\nSelect an Alert:\n\t1. SignalFX \n\t2. Splunk ITSI \n\t3. Splunk Core \n\t4. Splunk ES\n\t5. Datadog\n>'))
		#SignalFX
		if userIn == 1:
			post_alert(signalfx)
		#Splunk ITSI
		elif userIn == 2:
			post_alert(splunk_itsi)
		#Splunk Core
		elif userIn	== 3:
			post_alert(splunk_core)
		#Splunk ES
		elif userIn == 4:
			post_alert(splunk_es)
		#Datadog
		elif userIn == 5:
			post_alert(datadog)
		# Exit
		elif userIn == 0:
			sys.exit()
		else:
			print('invalid input')

if __name__ == '__main__':
	main()


