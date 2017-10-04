import {
    Widget
} from '@phosphor/widgets';

import {
    JupyterLab, JupyterLabPlugin, ILayoutRestorer
} from '@jupyterlab/application';

import {
    ICommandPalette
} from '@jupyterlab/apputils';

import {
    Session
} from '@jupyterlab/services';

import '../style/index.css';

const widget_id = 'taucmdr_project_selector';

interface IProjectsResult {
    readonly Name: string;
    readonly Targets: string;
    readonly Applications: string;
    readonly Measurements: string;
    readonly Experiments: string;
    readonly Selected: boolean;
    readonly [propName: string]: any;
};

class ProjectSelectorWidget extends Widget {

    readonly session_path: string = 'taucmdr.ipynb';

    readonly get_projects_kernel: string = `
import json
from taucmdr.model.project import Project
selected_name = None 
try:
    selected_name = Project.selected()['name']
except:
    pass
projects = [proj.populate() for proj in Project.controller().all()]
entries = []
for proj in projects:
    entry = {}
    entry['Name'] = proj['name']
    entry['Targets'] = ", ".join([target['name'] for target in proj['targets']])
    entry['Applications'] = ", ".join([app['name'] for app in proj['applications']])
    entry['Measurements'] = ", ".join([meas['name'] for meas in proj['measurements']])
    entry['Experiments'] = len(proj['experiments'])
    entry['Selected'] = True if selected_name == proj['name'] else False
    entries.append(entry)
print(json.dumps(entries))
`;

    readonly fields = ['Name', 'Targets', 'Applications', 'Measurements', 'Experiments'];

    contentDiv: HTMLDivElement;
    table: HTMLTableElement;
    tHead: HTMLTableSectionElement;
    tBody: HTMLTableSectionElement;
    tHeadRow: HTMLTableRowElement;
    session: Session.ISession;

    constructor() {
        super();
        this.id = widget_id;
        this.title.label = 'Projects';
        this.title.closable = true;
        this.addClass(widget_id);

        this.contentDiv = document.createElement("div");
        let button = document.createElement('button');
        button.appendChild(document.createTextNode("Refresh project list"));
        button.addEventListener('click', () => {this.list_projects()});
        this.contentDiv.appendChild(button);
        this.node.appendChild(this.contentDiv);
        this.table = document.createElement('table');
        this.table.className = 'table';
        this.build_header();
        this.tBody = this.table.createTBody();
        this.contentDiv.appendChild(this.table)
    };

    build_header(): void {
        this.tHead = this.table.createTHead();
        this.tHeadRow = this.tHead.insertRow();
        let firstCol = document.createElement('th');
        firstCol.className = 'empty';
        this.tHeadRow.appendChild(firstCol)
        this.fields.forEach( field => {
            let headerCol = document.createElement('th');
            headerCol.appendChild(document.createTextNode(field));
            this.tHeadRow.appendChild(headerCol);
        });
    }

    start_session(): Promise<Session.ISession> {
        if(!this.session) {
            return Session.findByPath(this.session_path).then(model => {
                return Session.connectTo(model.id).then(s => {
                    this.session = s;
                    return this.session;
                });
            }, () => {
                let options: Session.IOptions = {
                    kernelName: 'python',
                    path: this.session_path
                };
                return Session.startNew(options).then(s => {
                    this.session = s;
                    return this.session;
                }, r => {
                    throw new Error("Unable to start session")
                });
            })
        } else {
            return Promise.resolve(this.session);
        }
    };

    select_project(name : string) : void {
        console.log(`Should select ${name}`);
        let kernel_code = `
from taucmdr.model.project import Project
proj = Project.controller().one({"name": "${name}"})
Project.controller().select(proj)
`;
        this.start_session().then(s => {
            let future = this.session.kernel.requestExecute({code: kernel_code});
            future.onIOPub = msg => {
                console.log(msg);
                if (msg.header.msg_type == "stream") {
                    console.log(msg.content.text.toString());
                } else if(msg.header.msg_type == "status" && msg.content.execution_state == "idle") {
                    console.log("Selection complete")
                    this.list_projects();
                }
            };
        }, r => {
            console.error("Unable to select project: " + r.toString());
        });
    }

    list_projects(): void {
        let result : string = "";
        this.tBody.innerHTML = "";
        this.start_session().then(s => {
            let future = this.session.kernel.requestExecute({code: this.get_projects_kernel});
            future.onIOPub = msg => {
                console.log(msg);
                if (msg.header.msg_type == "stream") {
                    result = result.concat(msg.content.text.toString());
                } else if(msg.header.msg_type == "status" && msg.content.execution_state == "idle") {
                    let projects: Array<IProjectsResult> = JSON.parse(result);
                    projects.forEach(project => {
                        let row = this.tBody.insertRow();
                        let button = document.createElement('button');
                        button.className = 'select';
                        button.id = project.Name;
                        button.addEventListener('click', event => {
                            this.select_project((<HTMLElement>(event.target)).id);
                        });
                        button.appendChild(document.createTextNode('Select'));
                        if(project.Selected) {
                            button.disabled = true;
                            row.className = 'selected';
                        }
                        let firstCell = row.insertCell();
                        firstCell.className = 'edit-buttons';
                        firstCell.appendChild(button);
                        this.fields.forEach(field => {
                            let cell = row.insertCell();
                            cell.appendChild(document.createTextNode(project[field]));
                        });
                    });
                }
            };
        }, r => {
            console.error("Unable to get project list: " + r.toString())
        });
    };
}

function activate(app: JupyterLab, palette: ICommandPalette, restorer: ILayoutRestorer) {
    // Declare a widget variable
    let widget: ProjectSelectorWidget;

    widget = new ProjectSelectorWidget();

    app.shell.addToLeftArea(widget, {rank: 1000});

    restorer.add(widget, widget_id);
}

/**
 * Initialization data for the jupyterlab_xkcd extension.
 */
const extension: JupyterLabPlugin<void> = {
    id: widget_id,
    autoStart: true,
    requires: [ICommandPalette, ILayoutRestorer],
    activate: activate
};

export default extension;