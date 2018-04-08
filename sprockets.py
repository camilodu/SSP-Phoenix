from storage_container import StorageContainer
from vm import VM
from tasks import Tasks
from health_checks import HealthChecks

def main():
    container = StorageContainer.get_storage_container("NutanixManagementShare")
    container.enable_compression()

    #vm = VM(VM.get_vm("DB Server"))
    #ips = vm.get_ips()
    #print ips

    #tasks = Task.get_tasks()

    #for task in tasks:
    #    print task

    #health_checks = HealthChecks.get_health_checks()
    #for health_check in health_checks:
    #     print health_check
    #print len(health_checks)
    return 0


if __name__ == "__main__":
    main()
