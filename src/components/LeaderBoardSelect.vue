<template>
  <div class="row select-row">
    <div class="col col-auto left-select">
      <button type="button" class="btn btn-success responsive-text" data-bs-toggle="modal" data-bs-target="#selectModal">
        Task Select
      </button>
      <div class="modal fade" id="selectModal" tabindex="-1" aria-labelledby="selectModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content">
            <div class="modal-header-part">
              <p class="modal-header-title-name" id="selectModalLabel">
                Please select specific task and operation.
              </p>
            </div>
            <div class="modal-body">
              <div class="card">
                <div class="card-body">
                  <div class="row">
                    <div class="col-2">Task:</div>
                    <div class="col-10">
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" name="taskRadio" id="taskRadio1"
                          value="CognitiveDiagnosis" v-model="selectedTask" />
                        <label class="form-check-label" for="taskRadio1">
                          Cognitive Diagnosis
                        </label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" name="taskRadio" id="taskRadio2"
                          value="KnowledgeTracing" v-model="selectedTask" />
                        <label class="form-check-label" for="taskRadio2">
                          Knowledge Tracing
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="card">
                <div class="card-body">
                  <div class="row">
                    <div class="col-2">Dataset:</div>
                    <div class="col-10">
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" name="datasetRadio" id="datasetRadio1" value="FrcSub"
                          v-model="selectedDataset" />
                        <label class="form-check-label" for="datasetRadio1">
                          FrcSub
                        </label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" name="datasetRadio" id="datasetRadio2"
                          value="ASSISTment0910" v-model="selectedDataset" />
                        <label class="form-check-label" for="datasetRadio2">
                          ASSISTment0910
                        </label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" name="datasetRadio" id="datasetRadio3" value="Junyi"
                          v-model="selectedDataset" />
                        <label class="form-check-label" for="datasetRadio3">
                          Junyi
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="card">
                <div class="card-body">
                  <div class="row">
                    <div class="col-2">Application:</div>
                    <div class="col-10">
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" name="applyRadio" id="applyRadio1" value="General"
                          v-model="selectedApplication" />
                        <label class="form-check-label" for="applyRadio1">
                          General
                        </label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" name="applyRadio" id="applyRadio2"
                          value="KnowledgeMissing" v-model="selectedApplication" />
                        <label class="form-check-label" for="applyRadio1">
                          KnowledgeMissing
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                Close
              </button>
              <button @click="refresh" type="button" class="btn btn-primary" data-bs-dismiss="modal">
                Refersh
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-sm right-show-content">
      <div v-if="showContext.is_showed" class="card right-card-show">
        <div class="card-body right-card-body-show">
          <p class="right-card-body-show-content">
            Task: {{ showContext.task }} | Dataset: {{ showContext.dataset }} | Application: {{ showContext.application }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  name: "LeaderBoardSelect",
  props: {
    showContext: {
      type: Object,
      required: true,
    },
  },
  setup(props, context) {
    let selectedTask = ref("");
    let selectedDataset = ref("");
    let selectedApplication = ref("");

    const refresh = () => {
      context.emit("refresh", selectedTask.value, selectedDataset.value, selectedApplication.value);
    };

    return {
      selectedTask,
      selectedDataset,
      selectedApplication,
      refresh,
    };
  },
};
</script>

<style scoped>
@media (max-width: 1400px) and (min-width: 500px) {
  .right-card-body-show-content {
    font-size: calc(3px + 1vw);

  }
}

.right-card-body-show-content {
  margin: 0px;
  font-weight: bold;
  color: #23272E;
}

.right-card-body-show {
  padding: 0px;
  padding-top: 4px;
  padding-bottom: 4px;
  padding-left: 6px;
}

.right-card-show {
  margin-top: 3px;
  margin-right: 12px;
  display: flex;
}

.modal-header-part {
  padding: 10px;
}

.modal-header-title-name {
  font-size: 15px;
  margin-bottom: 0px;
  color: gray;
}

@media (max-width: 1400px) and (min-width: 500px) {
  .responsive-text {
    white-space: nowrap;
    word-wrap: break-word;
    word-break: break-all;
    font-size: calc(3px + 1vw);
  }
}

.right-show-content {
  padding: 0px;
}

.select-row {
  margin-top: 0px;
}
</style>