export interface Employee {
    crm_id: string;
    portal_id: number;
    first_name: string;
    last_name: string;
    middle_name: string;
    job_title: string;
    image: string;
    mobile: string;
    phone: string;
    email: string;
    skype: string;
    head: Employee;
}
