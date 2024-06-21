import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-json-viewer',
  template: `
    <ul *ngIf="data; else valueTemplate">
      <li *ngFor="let key of objectKeys(data)">
        <div *ngIf="isObject(data[key]); else valueItem">
          <strong>{{ key }}:</strong>
          <app-json-viewer [data]="data[key]"></app-json-viewer>
        </div>
        <ng-template #valueItem>
          <strong>{{ key }}:</strong>
          <i>{{ data[key] }}</i>
        </ng-template>
      </li>
    </ul>
    <ng-template #valueTemplate>{{ data }}</ng-template>
  `,
  styles: [`
    ul {
      list-style-type: none;
      padding-left: 1em;
      border-left: 1px solid #ddd;
      margin-bottom: 1em;
    }
  `]
})
export class JsonViewerComponent {
  @Input() data: any;

  ngOnInit() {

    console.log("🚀 ~ JsonViewerComponent ~ this.data:", this.data)
  }

  objectKeys = Object.keys;

  isObject(item) {
    return typeof item === 'object' && !Array.isArray(item);
  }
}
