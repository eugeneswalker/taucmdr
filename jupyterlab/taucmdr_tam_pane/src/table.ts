/* Copyright (c) 2017, ParaTools, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 * (1) Redistributions of source code must retain the above copyright notice,
 *     this list of conditions and the following disclaimer.
 * (2) Redistributions in binary form must reproduce the above copyright notice,
 *     this list of conditions and the following disclaimer in the documentation
 *     and/or other materials provided with the distribution.
 * (3) Neither the name of ParaTools, Inc. nor the names of its contributors may
 *     be used to endorse or promote products derived from this software without
 *     specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */


import {Kernels} from "./kernels";
import JSONResult = Kernels.JSONResult;

import '../style/index.css'

export class Table {
    protected data : Array<JSONResult>;
    protected fields : Array<string>;
    protected table_class : string;
    protected table : HTMLTableElement;
    protected footer : HTMLTableRowElement;
    protected cols : number;
    protected selectable : boolean;
    protected primary_key : string;
    protected checkboxes : Array<HTMLInputElement>;

    constructor(data : Array<JSONResult>, fields : Array<string>, table_class : string, selectable : boolean,
                primary_key : string) {
        this.data = data;
        this.fields = fields;
        this.table_class = table_class;
        this.selectable = selectable;
        this.primary_key = primary_key;
        this.cols = this.fields == null ? 0 : this.fields.length;
        if(this.selectable) {
            ++this.cols;
        }
        this.checkboxes = [];
        this.update_table();
    }

    protected update_table() {
        this.table = document.createElement('table');
        this.table.className = this.table_class;
        let tHead = this.table.createTHead();
        let tBody = this.table.createTBody();
        let tFoot = this.table.createTFoot();
        this.footer = tFoot.insertRow();

        let tHeadRow = tHead.insertRow();

        if(this.fields != null) {
            if(this.selectable) {
                // Header column for checkbox
                let cell = document.createElement('th');
                let checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.addEventListener('click', () => {
                    this.checkboxes.forEach(row_checkbox => {
                        row_checkbox.checked = checkbox.checked;
                    });
                });
                cell.appendChild(checkbox);
                tHeadRow.appendChild(cell);
            }
            this.fields.forEach(field => {
                let cell = document.createElement('th');
                cell.appendChild(document.createTextNode(field));
                tHeadRow.appendChild(cell);
            });

            this.data.forEach(rowData => {
                let row = tBody.insertRow();
                let checkbox : HTMLInputElement;
                if(this.selectable) {
                    let checkboxCell = row.insertCell();
                    checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.id = rowData[this.primary_key];
                    checkbox.name = 'selection';
                    checkbox.value = checkbox.id;
                    checkboxCell.appendChild(checkbox);
                    this.checkboxes.push(checkbox);
                    row.appendChild(checkboxCell);
                }
                this.fields.forEach(field => {
                    let cell = row.insertCell();
                    let value = rowData[field];
                    if (value == null) {
                        value = "N/A";
                    }
                    if(this.selectable) {
                        cell.addEventListener('click', () => {
                            checkbox.checked = !checkbox.checked;
                        });
                    }
                    cell.appendChild(document.createTextNode(value));
                    row.appendChild(cell);
                });
            });
        }
    }

    get_table() : HTMLTableElement {
        return this.table;
    }

    get_footer() : HTMLTableRowElement {
        return this.footer;
    }

    add_as_footer_row(element : HTMLElement) : void {
        let cell = this.footer.insertCell();
        cell.appendChild(element);
        cell.colSpan = this.cols;
    }

    get_selected() : Array<string> {
        let result : Array<string> = [];
        if(this.selectable) {
            this.checkboxes.forEach(checkbox => {
                if(checkbox.checked) {
                    result.push(checkbox.value);
                }
            });
        }
        return result;

    }
}