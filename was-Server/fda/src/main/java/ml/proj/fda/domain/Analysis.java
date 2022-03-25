package ml.proj.fda.domain;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class Analysis {

    private String city;
    private String district;
    private Long pollution_factor_score;
    private Long prospect;

    public Analysis(String city, String district, Long pollution_factor_score, Long prospect) {
        this.city = city;
        this.district = district;
        this.pollution_factor_score = pollution_factor_score;
        this.prospect = prospect;
    }
}
