// excel
function processExcel() {
  const fileUpload = document.getElementById('fileUpload');
  const file = fileUpload.files[0];
  const reader = new FileReader();

  reader.onload = function(e) {
    const data = new Uint8Array(e.target.result);
    const workbook = XLSX.read(data, { type: 'array' });
    const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
    const jsonData = XLSX.utils.sheet_to_json(firstSheet, { header: 1 });
    
    populateTable(jsonData);
  };

  reader.readAsArrayBuffer(file);
}

function populateTable(data) {
  const tableBody = document.querySelector('#bangdiem tbody');
  tableBody.innerHTML = ''; // Clear existing data

  data.forEach((row, index) => {
    if (index === 0) return; // Skip header row

    const tr = document.createElement('tr');
    row.forEach(cell => {
      const td = document.createElement('td');
      td.textContent = cell;
      tr.appendChild(td);
    });
    tableBody.appendChild(tr);
  });
}

// tinh GPA
function tinhGPA() {
  const table = document.getElementById('bangdiem').getElementsByTagName('tbody')[0];
  const rowCount = table.rows.length;

  let totalTinChi = 0;
  let totalDiem = 0;
  const monHocDetails = [];

  for (let i = 0; i < rowCount; i++) {
    const mamonHoc = table.rows[i].cells[1].textContent;
    const monHoc = table.rows[i].cells[2].textContent;
    const diemSo = parseFloat(table.rows[i].cells[3].textContent);
    const tinChi = parseFloat(table.rows[i].cells[4].textContent);
    

    if (!isNaN(tinChi) && !isNaN(diemSo) && diemSo >= 4.0) {
      totalTinChi += tinChi;
      totalDiem += tinChi * diemSo;
    }
    monHocDetails.push({ mamonHoc, monHoc, diemSo ,tinChi});
  }

  const gpa = totalDiem / totalTinChi;
  localStorage.setItem('gpa', gpa.toFixed(2));
  const nganh = document.getElementById('nganh').value;
  const nienkhoa = document.getElementById('nienkhoa').value;
  localStorage.setItem('totalTinChi', totalTinChi);
  localStorage.setItem('monHocDetails', JSON.stringify(monHocDetails));

  fetch('/upload_excel', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      gpa: gpa.toFixed(2),
      nganh: nganh,
      nienkhoa: nienkhoa,
      totalTinChi: totalTinChi,
      monHocDetails: monHocDetails
    }),
  })
  .then(response => response.json())
  .then(data => {
    console.log('Response from server:', data);
    // Redirect to ketqua or handle response if needed
    window.location.href = "/ketqua.html";
  })
  .catch(error => {
    console.error('Error:', error);
  });
  // Redirect to ketqua
  window.location.href = "/ketqua.html";
}

// Tải lên chương trình đào tạo
function loadChuongTrinhDaoTao() {
  const nganh = document.getElementById('nganh').value;
  const nienkhoa = document.getElementById('nienkhoa').value;

  fetch(`/api/chuongtrinhdaotao?nganh=${nganh}&nienkhoa=${nienkhoa}`)
    .then(response => response.json())
    .then(data => {
      const table = document.getElementById('chuongtrinhdaotao').getElementsByTagName('tbody')[0];
      table.innerHTML = ''; // Clear old content

      data.forEach(item => {
        const newRow = table.insertRow();

        newRow.insertCell(0).innerHTML = item['stt'];
        newRow.insertCell(1).innerHTML = item['Mã HP'];
        newRow.insertCell(2).innerHTML = item['Tên HP'];
        newRow.insertCell(3).innerHTML = item['Số TC'];
        newRow.insertCell(4).innerHTML = item['Ngành'];
        newRow.insertCell(5).innerHTML = item['Khóa'];
        newRow.insertCell(6).innerHTML = item['Kiểu môn'];
      });
    });
}

// Bảng ở trang ketqua
function hienThiKetQua() {
  const gpa = localStorage.getItem('gpa');
  const totalTinChi = localStorage.getItem('totalTinChi');
  const monHocDetails = JSON.parse(localStorage.getItem('monHocDetails'));

  if (gpa && monHocDetails) {
    document.getElementById('gpa').innerText = gpa;
    document.getElementById('tinchi').innerText = totalTinChi;

    const tableBody = document.querySelector('#bangdiemketqua tbody');
    tableBody.innerHTML = ''; // Clear existing data

    monHocDetails.forEach(detail => {
      const tr = document.createElement('tr');
      Object.values(detail).forEach(cell => {
        const td = document.createElement('td');
        td.textContent = cell;
        
        tr.appendChild(td);
      });
      if (detail.diemSo < 4.0) {
        tr.style.backgroundColor = 'red';
      }
      tableBody.appendChild(tr);
      
    });
  }
}


document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('gpa')) {
    hienThiKetQua();
  }
});


function vebieudo() {
  fetch('/vebieudo')
      .then(response => response.json())
      .then(data => {
        var bieuDoDiv = document.getElementById('bieu-do');
        bieuDoDiv.innerHTML = '';  // Xóa nội dung cũ

        data.file_paths.forEach(function(filePath) {
            var img = document.createElement('img');
            img.src = filePath + '?' + new Date().getTime();  // Thêm timestamp để tránh cache
            bieuDoDiv.appendChild(img);  // Hiển thị hình ảnh biểu đồ
        });
      })
      .catch(error => console.error('Error:', error));
}
function sosanh() {
  var maMonHoc = document.getElementById('ma-mon-hoc').value;
  fetch('/sosanh', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'ma-mon-hoc=' + maMonHoc
  })
  .then(response => response.json())
  .then(data => {
      var bieuDoDiv = document.getElementById('bieu-do');
      var img = document.createElement('img');
      img.src = data.file_path + '?' + new Date().getTime();  // Thêm timestamp để tránh cache
      bieuDoDiv.innerHTML = '';  // Xóa nội dung cũ
      bieuDoDiv.appendChild(img);  // Hiển thị hình ảnh biểu đồ

      var ketQuaDiv = document.getElementById('ket-qua');
      ketQuaDiv.innerText = data.result; 
  })
  .catch(error => console.error('Lỗi:', error));
}

function show_image() {
  fetch('/show_image')
      .then(response => response.json())
      .then(data => {
          document.getElementById('image-container').src = data.image_url;
      })
      .catch(error => console.error('Error:', error));
}