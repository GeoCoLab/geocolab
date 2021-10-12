import axios from '../_snowpack/pkg/axios.v0.22.0.js';
import $ from '../_snowpack/pkg/jquery.v3.6.0.js';


$(document).ready(() => {
    let csrf = $('#csrf_token').val();
    axios.defaults.headers.common['X-CSRFToken'] = csrf;

    let appId = $('#application_id').val();

    axios({
        method: 'get',
        url: `/apply/${ appId }/find_matches`
    }).then(r => {
        let matchesSection = $('#matches');
        if (r.data.success) {
            r.data.matches.map(m => {
                matchesSection.append(
                    `
                <div class="match-box max-w-md mb-8">
                  <p class="text-xl">
                    Facility in ${ m.location }
                  </p>
                  <div class="detail-container mb-8">
                    <div class="detail-row">
                      <span class="detail-row-header">Provides</span>
                      <span>${ [...m.matching_analyses, m.other_analyses].join('<br>') }</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-row-header">Next available</span>
                      <span>${ m.available } to ${ m.until }</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-row-header">Funding available</span>
                      <span>${ m.funding_level }</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-row-header">Visit/send samples</span>
                      <span>${ m.access_types }</span>
                    </div>
                  </div>
                  <input type="submit" data-slot-id="${ m.slot_id }" data-date-from="${ m.available }" data-date-to="${ m.until }" class="match-button p-2" value="Accept">
                </div>
                `
                );
            });
        }
        else {
            matchesSection.append('No matches:<br>' + r.data.errors.join('<br>'))
        }
    }).then(() => {
        $('.match-button').click(e => {
            axios.post('/apply/make_match', {
                    app_id: appId,
                    slot_id: e.target.dataset.slotId,
                    date_from: e.target.dataset.dateFrom,
                    date_to: e.target.dataset.dateTo
                }
            ).then((r) => {
                console.log(r);
                window.location.reload(true);
            });
        });
    });
});

