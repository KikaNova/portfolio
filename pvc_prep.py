from kubernetes import config,client
from colorama import Fore, Back, Style, init
import sys
import csv
from kubernetes.client.rest import ApiException
from pprint import pprint

def list_kube_contexts():
    # Load all contexts from kubeconfig
    contexts, active_context = config.list_kube_config_contexts()
    
    # Display the available contexts
    print(Fore.BLUE +"Available contexts:"+Style.RESET_ALL)
    for index, context in enumerate(contexts):
        active_marker = "(Active)" if context['name'] == active_context['name'] else ""
        print(f"{index + 1}. {context['name']} {Fore.GREEN} {active_marker} {Style.RESET_ALL}")

    return contexts, active_context['name']

def switch_kube_context():
    # List the contexts and get user input
    contexts, current_context = list_kube_contexts()
    
    # Prompt the user to choose a context by index
    user_input = input(f"\nEnter the number of the context you want to switch to (Press Enter to keep '{current_context}'): ")
    
    # If the user presses Enter without inputting anything, don't change the context
    if user_input.strip() == "":
        print(f"{Fore.GREEN}No change made. Keeping the current context: {current_context} {Style.RESET_ALL}")
        config.load_kube_config(context=current_context)
        return
    
    # Validate the input
    try:
        choice = int(user_input) - 1
        if choice < 0 or choice >= len(contexts):
            print(Fore.RED+"Invalid choice. Please select a number from the list."+Style.RESET_ALL)
            sys.exit(1)
    except ValueError:
        print(Fore.RED+"Invalid input. Please enter a number."+Style.RESET_ALL)
        sys.exit(1)
    
    # Get the selected context name
    selected_context = contexts[choice]['name']
    
    # Switch to the selected context
    config.load_kube_config(context=selected_context)
    print(f"{Fore.GREEN}Switched to context: {selected_context}")
    print(Fore.BLUE+"[Note] This change only impacts the lifetime of this script"+Style.RESET_ALL)

def getDeployments(namespace):
    v1_apps = client.CoreV1Api()
    # v1_autoscaling = client.AutoscalingV1Api()
    
    pvc_list = v1_apps.list_namespaced_persistent_volume_claim(namespace)

    with open(namespace+'.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["NAME","STORAGE CLASS","STORAGE AMOUNT"])
        
        for pvc in pvc_list.items:
            pvc_name = pvc.metadata.name
            print(f"PVC Name: {pvc_name}")
            print(pvc.status)
            storage_amount = pvc.spec.resources.requests.get("storage")
            print(f"Storage amount: {storage_amount}")
            storage_class = pvc.spec.storage_class_name
            print(f"Storage class: {storage_class}")

            spamwriter.writerow([pvc_name, storage_class, storage_amount])
    


if __name__ == "__main__":
    # kube config switch for the scope of the script
    switch_kube_context()
    # Get input for the namespace to check
    # namespace=input("Please type the full namespace name (Due to limited access i can't provide a list):" )
    namespace = "ho-it-sst1-i-cw-cwi"
    #v1 = client.CoreV1Api()
    #print("Listing pods with their IPs:")
    #ret = v1.list_namespaced_pod(namespace=namespace,watch=False)
    #for i in ret.items:
    #ß    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    print("Collecting data.....")
    getDeployments(namespace)
    print("Complete!")