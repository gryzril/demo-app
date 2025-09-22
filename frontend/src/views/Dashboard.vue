<template>
  <div class="p-6 space-y-4">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-semibold">Dashboard</h1>
      <div class="flex items-center gap-2">
        <Button label="New Task" icon="pi pi-plus" @click="openCreate()" />
        <Button label="Refresh" icon="pi pi-refresh" severity="secondary" @click="load()" :loading="loading" />
      </div>
    </div>

    <DataTable :value="tasks" data-key="id" :loading="loading" paginator :rows="10" responsive-layout="scroll">
      <Column field="title" header="Title" />
      <Column field="status" header="Status" />
      <Column field="due_date" header="Due">
        <template #body="{ data }">{{ fmtDate(data.due_date) }}</template>
      </Column>
      <Column header="Actions" style="width:10rem; min-width:8rem">
        <template #body="{ data }">
          <div class="flex justify-center">
            <Button
              icon="pi pi-trash"
              severity="danger"
              variant="outlined"
              rounded
              @click="remove(data.id)"
            />
          </div>
        </template>
      </Column>
    </DataTable>

    <Dialog v-model:visible="showCreate" header="Create Task" modal :style="{ width: '32rem' }">
      <div class="form-grid">
        <label for="title">Title</label>
        <InputText id="title" v-model="form.title" />

        <label for="desc">Description</label>
        <Textarea id="desc" v-model="form.description" rows="3" />

        <label for="status">Status</label>
        <Dropdown id="status" v-model="form.status" :options="statuses" optionLabel="label" optionValue="value" />

        <label for="due">Due date</label>
        <Calendar id="due" v-model="form.due_date" showIcon />
      </div>

      <template #footer>
        <div class="w-full flex justify-end gap-2">
          <Button label="Cancel" severity="secondary" @click="showCreate = false" />
          <Button label="Create" :loading="creating" @click="create()" />
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useToast } from "primevue/usetoast";
import Button from "primevue/button";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import Textarea from "primevue/textarea"
import Dropdown from "primevue/dropdown";
import Calendar from "primevue/calendar";
import { getAllTasks, getTask, createTask, updateTask, deleteTask } from "@/api/tasks"
import type { TaskCreate, TaskUpdate, Status, Task } from "@/api/entities/Tasks";

const toast = useToast();
const tasks = ref<Task[]>([]);
const loading = ref(false);

const showCreate = ref(false);
const creating = ref(false);
const statuses = [
  { label: "Todo", value: "todo" },
  { label: "Doing", value: "doing" },
  { label: "Done", value: "done" },
];

const form = ref<{ title: string; description?: string; status: Task["status"]; due_date: Date | null }>({
  title: "",
  description: "",
  status: "todo",
  due_date: null,
});

async function load() {
  loading.value = true;
  try {
    const data = await getAllTasks();
    tasks.value = data;
  } catch (err: any) {
    toast.add({ severity: "error", summary: "Load failed", detail: err?.message ?? "Error" });
  } finally {
    loading.value = false;
  }
}

function openCreate() {
  form.value = { title: "", description: "", status: "todo", due_date: null };
  showCreate.value = true;
}

async function create() {
  if (!form.value.title) {
    toast.add({ severity: "warn", summary: "Title required" });
    return;
  }
  creating.value = true;
  const payload: TaskCreate = {
    title: form.value.title,
    description: form.value.description || null,
    status: form.value.status,
    due_date: form.value.due_date ? form.value.due_date.toISOString() : null,
    label_ids: [] as number[],
  };
  try {
    const t = await createTask(payload)
    tasks.value = [t, ...tasks.value]; // optimistic insert
    showCreate.value = false;
    toast.add({ severity: "success", summary: "Task created" });
  } catch (err: any) {
    toast.add({ severity: "error", summary: "Create failed", detail: err?.message ?? "Error" });
  } finally {
    creating.value = false;
  }
}

async function remove(id: number) {
  const prev = tasks.value.slice();
  tasks.value = tasks.value.filter((x) => x.id !== id);
  try {
    await deleteTask(id);
    toast.add({ severity: "info", summary: "Task deleted" });
  } catch (err: any) {
    tasks.value = prev; // rollback
    toast.add({ severity: "error", summary: "Delete failed", detail: err?.message ?? "Error" });
  }
}

function fmtDate(s?: string | null) {
  if (!s) return "";
  const d = new Date(s);
  return d.toLocaleDateString();
}

onMounted(load);
</script>

<style scoped>
.form-grid {
  display: grid;
  grid-template-columns: 110px 1fr;
  align-items: center;
  row-gap: 14px;
  column-gap: 12px;
}
.form-grid :deep(.p-inputtext),
.form-grid :deep(.p-textarea),
.form-grid :deep(.p-dropdown),
.form-grid :deep(.p-calendar),
.form-grid :deep(.p-inputwrapper) {
  width: 100%;
}
</style>