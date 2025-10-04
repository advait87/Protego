# PROTEGO_WINDOWS/utils/reporting.py

import datetime
import os

def create_compliance_report(check_results, command, output_filename, level="strict"):
    """Generates a detailed compliance report (TXT format)."""
    output_path = os.path.join(os.getcwd(), output_filename)
    
    report_data = f"--- Protego Compliance Report: {command} ---\n"
    report_data += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report_data += f"Hardening Level: {level}\n"
    report_data += "=" * 50 + "\n"
    
    compliant_count = 0
    noncompliant_count = 0

    for result in check_results:
        status = result.get('status', 'N/A')
        
        if status == 'COMPLIANT' or status == 'SUCCESS':
            compliant_count += 1
            status_text = "SUCCESS"
        else:
            noncompliant_count += 1
            status_text = "FAILURE"

        report_data += f"POLICY: {result['policy']}\n"
        report_data += f"  Status: {status_text}\n"
        report_data += f"  Previous/State: {result.get('previous', 'N/A')}\n"
        report_data += f"  Current/Final: {result.get('current', 'N/A')}\n"
        report_data += f"  Target Value: {result.get('target', 'N/A')}\n"
        report_data += "-" * 50 + "\n"
        
    report_data += f"\n--- Summary ---\n"
    report_data += f"Total Checks: {len(check_results)}\n"
    report_data += f"Compliant/Success: {compliant_count}\n"
    report_data += f"Non-Compliant/Failure: {noncompliant_count}\n"


    with open(output_path, 'w') as f:
        f.write(report_data)
        
    print(f"\nReport generated successfully at: {output_path}")