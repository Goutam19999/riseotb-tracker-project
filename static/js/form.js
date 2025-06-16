
document.addEventListener('DOMContentLoaded', function() {
    const agentActionSelect = document.getElementById('id_agent_action');
    const selectedLabelsField = document.getElementById('id_selected_labels');
    const selectedLabelsLabel = document.querySelector('label[for="id_selected_labels"]');

    function updateSelectedLabelsVisibility() {
        const value = agentActionSelect.value;
        if (value === 'approved' || value === 'approved-Instagram Admin Rights Required') {
            selectedLabelsField.style.display = 'block';
            selectedLabelsLabel.textContent = "What label selected for the Post along with 'crm-trg-feed'?";
        } else if (value === 'rejected') {
            selectedLabelsField.style.display = 'block';
            selectedLabelsLabel.textContent = 'Reason for Rejection';
        } else {
            selectedLabelsField.style.display = 'none';
            selectedLabelsLabel.textContent = '';  // or original label if you want
        }
    }

    // Run on page load in case of initial value
    updateSelectedLabelsVisibility();

    // Listen for changes on agent_action field
    agentActionSelect.addEventListener('change', updateSelectedLabelsVisibility);
});
