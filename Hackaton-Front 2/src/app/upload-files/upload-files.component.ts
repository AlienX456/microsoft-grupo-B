import { Component, ElementRef, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { url } from 'inspector';

@Component({
  selector: 'app-upload-files',
  templateUrl: './upload-files.component.html',
  styleUrls: ['./upload-files.component.css']
})
export class UploadFilesComponent {
  data: any = {};
  selectedFiles: File[] = [];
  pdfsData : any = {"Status": "Pending"}
  disabled = false;
  useLLM : boolean = false;

  constructor(private http: HttpClient) { }

  onFileChange(event) {
    for (let [key, value] of Object.entries(event.target.files)) {
      this.selectedFiles.push(<File>event.target.files[key]);
    }
    console.log("🚀 ~ UploadFilesComponent ~ onFileChange ~ event:", event)
  };

  sendFile(event: Event) {
    let formData = new FormData();

    for (let index = 0; index < this.selectedFiles.length; index++) {
      const element = this.selectedFiles[index];
      formData.append('files', element, element.name);
    }

    this.data = "Momentico que ya casi..."

    // Descomenta la siguiente línea si quieres enviar formData a tu API
    console.log("useLLM:", this.useLLM)
    let url = 'http://localhost:8000/upload'
    if (!this.useLLM) {
      url = 'http://localhost:8000/upload?use_llm=false'
    }
    this.http.post(url, formData).subscribe(response => {
      this.data = response
      this.disabled = false;
    });
    this.disabled = true;

    for (let [key, value] of (<any>formData).entries()) {
      console.log(key, value);
    }
    this.selectedFiles = []
  };
}
