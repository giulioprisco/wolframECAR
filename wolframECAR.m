% Wolfram's Elementary Cellular Automata Simulator
% This script simulates the evolution of the elementary cellular automaton 
% for a hardcoded rule number, starting from a specified array of live cell positions.
% It uses periodic boundary conditions.
% The result is displayed as an image where black represents live cells (1)
% and white represents dead cells (0).
% Option to simulate reversible version as defined in Wolfram's NKS: prompted for input.
% Option to read initial from file, option to run backwards (requires reversible and file with two lines).

% Parameters
rule = 37;          % Hardcoded rule number (example: Rule 30)
generations = 1799;  % Number of generations to simulate
width = 2400;       % Fixed width of the grid
filename = 'cells.txt';  % File to save/read states
image_filename = 'ca_image.png';  % File to save the image

% Prompt for reversible mode
reversible = input('Enter 1 for reversible simulation, 0 for standard: ');

% Prompt for direction
backward = input('Enter 1 for backward simulation, 0 for forward: ');

if backward && ~reversible
    error('Backward simulation requires reversible mode.');
end

% Prompt for initial source
from_file = input('Enter 1 to read initial from file, 0 for hardcoded: ');

% Initialize the grid
grid = zeros(generations + 1, width);

% Set initial condition
if from_file
    fid = fopen(filename, 'r');
    if fid == -1
        error('Could not open file %s', filename);
    end
    if backward
        % Read two lines for backward: first prev, second curr
        line1 = fgetl(fid);
        line2 = fgetl(fid);
        if ~ischar(line1) || ~ischar(line2)
            error('File must have at least two lines for backward simulation.');
        end
        prev_positions = str2num(line1); %#ok<ST2NM>
        prev_positions = prev_positions(:)';
        curr_positions = str2num(line2); %#ok<ST2NM>
        curr_positions = curr_positions(:)';
        grid(1, curr_positions) = 1;  % Current (present)
        grid(2, prev_positions) = 1;  % Prev (recent past)
    else
        % For forward, read the last line as initial
        line = '';
        while ~feof(fid)
            temp_line = fgetl(fid);
            if ischar(temp_line)
                line = temp_line;
            end
        end
        curr_positions = str2num(line); %#ok<ST2NM>
        curr_positions = curr_positions(:)';
        grid(1, curr_positions) = 1;
    end
    fclose(fid);
else
    % Hardcoded
    curr_positions = [822, 827, 830, 838, 846, 847, 848, 855, 859, 860, 860, 861, 863, 868, 878, 878, 888, 895, 900, 911, 1125, 1128, 1136, 1138, 1140, 1148, 1158, 1167, 1169, 1171, 1171, 1173, 1195, 1195, 1198, 1199, 1208, 1210, 1213, 1214, 1223, 1224, 1227, 1227, 1230, 1235, 1237, 1242, 1245, 1262, 1271, 1272, 1288, 1293, 1293, 1295, 1298, 1308, 1311, 1317];  % General array of positions (1-based indices)
    grid(1, curr_positions) = 1;
end

% Extract the rule bits: rule_bits(k+1) gives the output for neighborhood k (0-7)
rule_bits = bitget(rule, 1:8);

% Simulate the automaton
if ~backward
    % Forward simulation
    for t = 1:generations
        for x = 1:width
            % Periodic boundaries
            left = mod(x-2, width) + 1;
            right = mod(x, width) + 1;
            left_val = grid(t, left);
            right_val = grid(t, right);
            
            % Compute neighborhood value (binary: left*4 + center*2 + right*1)
            neigh = left_val * 4 + grid(t, x) * 2 + right_val * 1;
            
            % Compute rule output
            rule_output = rule_bits(neigh + 1);
            
            % Set next state
            if reversible
                if t == 1
                    xor_term = 0;
                else
                    xor_term = grid(t - 1, x);
                end
                grid(t + 1, x) = bitxor(rule_output, xor_term);
            else
                grid(t + 1, x) = rule_output;
            end
        end
    end
else
    % Backward simulation (reversible only)
    % Grid(1,:) = curr, grid(2,:) = prev
    % Then grid(3,:) = rule(grid(2,:)) XOR grid(1,:)) = earlier
    for t = 2:generations
        for x = 1:width
            % Periodic boundaries
            left = mod(x-2, width) + 1;
            right = mod(x, width) + 1;
            left_val = grid(t, left);
            right_val = grid(t, right);
            
            % Compute neighborhood value (binary: left*4 + center*2 + right*1)
            neigh = left_val * 4 + grid(t, x) * 2 + right_val * 1;
            
            % Compute rule output
            rule_output = rule_bits(neigh + 1);
            
            % Set "next" which is earlier: XOR with "curr" grid(t-1,x)
            grid(t + 1, x) = bitxor(rule_output, grid(t - 1, x));
        end
    end
end

% Save the image without borders or legends
image_data = uint8((1 - grid) * 255);  % 0 -> 255 (white), 1 -> 0 (black)
imwrite(image_data, image_filename);

% Display the result
figure;
imagesc(grid);
colormap(flipud(gray));  % Flip colormap: 0=white, 1=black
if reversible
    mode_str = ' (Reversible)';
else
    mode_str = '';
end
if backward
    dir_str = ' Backward';
else
    dir_str = '';
end
% title(['Elementary Cellular Automaton - Rule ' num2str(rule) mode_str dir_str]);
xlabel('Cell Position');
ylabel('Generation');

% Save the final values to file
fid = fopen(filename, 'w');
if fid == -1
    error('Could not open file %s for writing', filename);
end
if reversible
    % Save second last and last
    second_last_pos = find(grid(end-1, :) == 1);
    last_pos = find(grid(end, :) == 1);
    fprintf(fid, '%d ', second_last_pos);
    fprintf(fid, '\n');
    fprintf(fid, '%d ', last_pos);
    fprintf(fid, '\n');
else
    % Save only last
    last_pos = find(grid(end, :) == 1);
    fprintf(fid, '%d ', last_pos);
    fprintf(fid, '\n');
end
fclose(fid);