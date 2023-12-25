use std::f64::consts::E;

/// A lookup table for target plate thickness based on certain criteria.
fn lookup_target_thickness(criteria: f64) -> f64 {
    // This should be filled with actual data later which I need to pull from WT
    let table = vec![
        (100.0, 1.0),
        (200.0, 2.0),
        (300.0, 3.0),
    ];

    // Find the thickness based on the criteria.
    for &(criterion, thickness) in &table {
        if criteria < criterion {
            return thickness;
        }
    }

    // Default thickness if no criteria is met.
    // This should be adjusted based on the actual default value required.
    10.0
}

/// Calculate penetration using the given formula and parameters.
///
/// # Parameters
/// - `l_w`: working length of penetrator material [mm]
/// - `p_p`: penetrator density [kg/m^3]
/// - `v_t`: impact velocity [km/s]
/// - `b_hnt`: Brinell Hardness Number of target
///
/// # Returns
/// - The penetration length in line of sight [mm]
fn calculate_penetration(
    l_w: f64,
    p_p: f64,
    v_t: f64,
    b_hnt: f64,
) -> f64 {
    // The criteria for selecting the thickness could be another parameter or calculated from existing ones.
    // For this example, we'll use the Brinell Hardness Number of the target as the criteria.
    let d = lookup_target_thickness(b_hnt); // Find the target plate thickness from the lookup table

    let b0 = 0.283;
    let b1 = 0.0656;
    let a = 0.921;
    let c0 = 138.0;
    let c1 = -0.10;

    // Calculate s^2 according to the given formula
    let s_squared = (c0 + c1 * b_hnt) * b_hnt / p_p;

    // Convert impact velocity to m/s from km/s for the formula
    let v_t_m_s = v_t * 1000.0;

    // Calculate the penetration P
    let p = a - (1.0 / (s_squared).tanh().powf(0.5 + b0 + b1 * (l_w / d))) * (p_p / v_t_m_s).sqrt();

    p
}

fn main() {
    // Example values for the parameters
    let l_w = 4.0; // Working length of penetrator material [mm]
    let p_p = 1.0; // Penetrator density [kg/m^3]
    let v_t = 1.0; // Impact velocity [km/s]
    let b_hnt = 200.0; // Brinell Hardness Number of target

    // Ensure that the Brinell Hardness Number Target is within the specified range
    assert!(b_hnt > 150.0 && b_hnt < 500.0, "BHNT must be between 150 and 500");

    let penetration = calculate_penetration(l_w, p_p, v_t, b_hnt);

    println!("Penetration: {} mm", penetration);
}
