<template>
  <div id="app" style="text-align: center;font-size: 24px;">
    <h1><b>学生信息管理系统</b></h1>
    <form @submit.prevent="addStudent">
      <input v-model="newStudent.name" placeholder="姓名" required>
      <input style="margin: 10px;"v-model="newStudent.student_id" placeholder="学号" required>
      <button type="submit" style="background-color: #c767ff; color: white; padding: 5px 10px; border: none; border-radius: 5px;">添加学生</button>
    </form>
    <input style="line-height: 2;width: 430px;" v-model="searchQuery" placeholder="搜索姓名或学号" @input="searchStudents">
    <table>
      <thead>
        <tr>
          <th>姓名</th>
          <th>学号</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in students" :key="student.id">
          <td>{{ student.name }}</td>
          <td>{{ student.student_id }}</td>
          <td>
            <button @click="editStudent(student.id)">编辑</button>
            <button @click="deleteStudent(student.id)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="selectedStudent">
      <form @submit.prevent="updateStudent">
        <input v-model="selectedStudent.name" placeholder="姓名">
        <input v-model="selectedStudent.student_id" placeholder="学号">
        <button type="submit">更新</button>
        <button @click="cancelEdit">取消</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      newStudent: { name: '', student_id: '' },
      selectedStudent: null,
      students: [],
      searchQuery: ''
    };
  },
  methods: {
    addStudent() {
      axios.post('http://localhost:5000/students', this.newStudent)
        .then(response => {
          this.students.push(response.data);
          this.newStudent = { name: '', student_id: '' };
        })
        .catch(error => console.error(error));
    },
    fetchStudents() {
      axios.get('http://localhost:5000/students')
        .then(response => {
          this.students = response.data;
        })
        .catch(error => console.error(error));
    },
    deleteStudent(id) {
      axios.delete(`http://localhost:5000/students/${id}`)
        .then(() => {
          this.fetchStudents();
        })
        .catch(error => console.error(error));
    },
    editStudent(id) {
      const student = this.students.find(student => student.id === id);
      this.selectedStudent = { ...student };
    },
    updateStudent() {
      axios.put(`http://localhost:5000/students/${this.selectedStudent.id}`, this.selectedStudent)
        .then(() => {
          this.fetchStudents();
          this.selectedStudent = null;
        })
        .catch(error => console.error(error));
    },
    cancelEdit() {
      this.selectedStudent = null;
    },
    searchStudents() {
      if (this.searchQuery) {
        axios.get(`http://localhost:5000/students?query=${this.searchQuery}`)
          .then(response => {
            this.students = response.data;
          })
          .catch(error => console.error(error));
      } else {
        this.fetchStudents();
      }
    }
  },
  created() {
    this.fetchStudents();
  }
};
</script>

<style>
#app {
  background-color: #4f4252; /* 例如，这里设置为白色 */
  /* 确保背景颜色应用到整个视口高度 */
  min-height: 100vh;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border: 1px solid #ffffff;
  padding: 8px;
}
th {
  background-color: #ffffff;
  text-align: left;
  color: black;
}
button {
  color: black;
  background-color: white;
  border: 1px solid #ddd;
  padding: 4px 8px;
  cursor: pointer;
}
button:hover {
  background-color: #c6c6c6;
}

</style>